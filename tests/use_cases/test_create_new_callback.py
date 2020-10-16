"""
These tests evaluate (and document) the business logic.
"""
import random
from datetime import datetime
from unittest import mock
from uuid import uuid4

from app.domain.entities.callback import Callback
from app.domain.entities.enrolment import Enrolment
from app.repositories.callback_repo import CallbackRepo
from app.repositories.enrolment_repo import EnrolmentRepo
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.callback_requests import CallbackRequest
from app.responses import FailureType, ResponseFailure, SuccessType
from app.use_cases.create_new_callback import CreateNewCallback

dummy_callback_id = str(uuid4())
dummy_enrolment_id = str(uuid4())
dummy_invalid_enrolment_id = str(uuid4())
dummy_shared_secret = str(uuid4())
dummy_invalid_shared_secret = str(uuid4())
dummy_received = datetime.now()
dummy_ref = "dummy_ref"
dummy_tp_ref = random.randint(0, 99999)
dummy_payload = {"data": "blbnjsd;fnbs"}


def test_create_new_callback_success():
    """
    When creating a new enrollment authorisation,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)
    callback = Callback(
        callback_id=dummy_callback_id,
        enrolment_id=dummy_enrolment_id,
        shared_secret=dummy_shared_secret,
        tp_sequence=dummy_tp_ref,
        received=dummy_received,
        payload=dummy_payload,
    )
    enrolment = Enrolment(
        created=datetime.now(),
        enrolment_id=dummy_enrolment_id,
        shared_secret=dummy_shared_secret,
        internal_reference=dummy_ref,
    )
    enrolment_repo.get_enrolment.return_value = enrolment
    repo.save_callback.return_value = callback

    request = CallbackRequest(
        enrolment_id=dummy_enrolment_id,
        shared_secret=dummy_shared_secret,
        tp_sequence=dummy_tp_ref,
        payload=dummy_payload,
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    assert response.type == SuccessType.SUCCESS
    assert response.message == "The callback has been saved."
    assert response.value.get("enrolment_id") == enrolment.enrolment_id
    assert response.value.get("shared_secret") == enrolment.shared_secret


def test_create_new_callback_failure():
    """
    When creating a new enrollment authorisation,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment = Enrolment(
        created=datetime.now(),
        enrolment_id=dummy_enrolment_id,
        shared_secret=dummy_shared_secret,
        internal_reference=dummy_ref,
    )
    enrolment_repo.get_enrolment.return_value = enrolment
    repo.save_callback.side_effect = Exception()

    request = CallbackRequest(
        enrolment_id=dummy_enrolment_id,
        shared_secret=dummy_shared_secret,
        tp_sequence=dummy_tp_ref,
        payload=dummy_payload,
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_called_once()
    assert response.type == FailureType.RESOURCE_ERROR


def test_create_new_callback_failure_on_invalid_enrolment_id():
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)

    error_message = (
        "NoSuchKey: An error occurred (NoSuchKey) when calling the GetObject operation: "
        "The specified key does not exist."
    )
    enrolment_repo.get_enrolment.return_value = (
        ResponseFailure.build_from_resource_error(message=error_message)
    )

    request = CallbackRequest(  # Send invalid enrolment ID
        enrolment_id=dummy_invalid_enrolment_id,
        shared_secret=dummy_shared_secret,
        tp_sequence=dummy_tp_ref,
        payload=dummy_payload,
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_not_called()
    assert response.type == FailureType.RESOURCE_ERROR
    assert response.message == error_message


def test_create_new_callback_failure_on_invalid_shared_secret():
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)

    enrolment = Enrolment(
        created=datetime.now(),
        enrolment_id=dummy_enrolment_id,
        shared_secret=dummy_shared_secret,
        internal_reference=dummy_ref,
    )
    enrolment_repo.get_enrolment.return_value = enrolment

    request = CallbackRequest(  # Send invalid key which doesn't match
        enrolment_id=dummy_enrolment_id,
        shared_secret=dummy_invalid_shared_secret,
        tp_sequence=dummy_tp_ref,
        payload=dummy_payload,
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_not_called()
    assert response.type == FailureType.RESOURCE_ERROR
    assert response.message == "'shared_secret' key doesn't match"
