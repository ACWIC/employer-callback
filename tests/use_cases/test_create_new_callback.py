"""
These tests evaluate (and document) the business logic.
"""
import random
from datetime import datetime
from unittest import mock
from unittest.mock import patch
from uuid import UUID, uuid4

from app.domain.entities.callback import Callback
from app.domain.entities.enrolment import Enrolment
from app.repositories.callback_repo import CallbackRepo
from app.repositories.enrolment_repo import EnrolmentRepo
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.callback_requests import CallbackRequest
from app.responses import FailureType, ResponseFailure, SuccessType
from app.use_cases.create_new_callback import CreateNewCallback


def test_create_new_callback_success():
    """
    When creating a new enrollment authorisation,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)
    # dummy data
    cb_id = uuid4()
    enrl_id = "dummy_enrolment_id"
    key = "dummy_enrolment_key"
    dummy_ref = "dummy_ref"
    tp_ref = random.randint(0, 99999)
    rx = datetime.now()
    pl = {"data": "blbnjsd;fnbs"}
    callback = Callback(
        callback_id=cb_id,
        enrolment_id=enrl_id,
        key=key,
        tp_sequence=tp_ref,
        received=rx,
        payload=pl,
    )
    enrolment = Enrolment(
        created=datetime.now(),
        enrolment_id=enrl_id,
        shared_secret=key,
        internal_reference=dummy_ref,
    )
    enrolment_repo.get_enrolment.return_value = enrolment
    repo.save_callback.return_value = callback

    request = CallbackRequest(
        enrolment_id=enrl_id, key=key, tp_sequence=tp_ref, payload=pl
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    assert response.type == SuccessType.SUCCESS
    assert response.value.get("enrolment_id") == enrolment.enrolment_id
    assert response.value.get("key") == enrolment.shared_secret


def test_create_new_callback_failure():
    """
    When creating a new enrollment authorisation,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=S3EnrolmentRepo)
    enrl_id = "dummy_enrolment_id"
    key = "dummy_enrolment_key"
    dummy_ref = "dummy_ref"
    tp_ref = 534
    pl = {"brace": "yourself"}
    enrolment = Enrolment(
        created=datetime.now(),
        enrolment_id=enrl_id,
        shared_secret=key,
        internal_reference=dummy_ref,
    )
    enrolment_repo.get_enrolment.return_value = enrolment
    repo.save_callback.side_effect = Exception()

    request = CallbackRequest(
        enrolment_id=enrl_id, key=key, tp_sequence=tp_ref, payload=pl
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_called_once()
    assert response.type == FailureType.RESOURCE_ERROR


@patch("uuid.uuid4")
def test_create_new_callback_failure_on_invalid_enrolment_id(patched_uuid4):
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)
    invalid_enrl_id = "9a778aac-09b0-48f3-bc5b-6710a60b8c6f"
    key = "c8894b4f-c160-40fa-8b2b-22a00ee49944"
    patched_uuid4.side_effect = [str(UUID(invalid_enrl_id)), str(UUID(key))]

    invalid_enrl_id = patched_uuid4()
    key = patched_uuid4()
    tp_ref = 534
    pl = {}
    error_message = (
        "NoSuchKey: An error occurred (NoSuchKey) when calling the GetObject operation: "
        "The specified key does not exist."
    )
    enrolment_repo.get_enrolment.return_value = (
        ResponseFailure.build_from_resource_error(message=error_message)
    )

    request = CallbackRequest(  # Send invalid enrolment ID
        enrolment_id=invalid_enrl_id,
        key=key,
        tp_sequence=tp_ref,
        payload=pl,
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_not_called()
    assert response.type == FailureType.RESOURCE_ERROR
    assert response.message == error_message


@patch("uuid.uuid4")
def test_create_new_callback_failure_on_invalid_shared_secret(patched_uuid4):
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)
    enrl_id = "75228a95-6bb6-4693-9673-dbd06b63ec7e"
    key = "c8894b4f-c160-40fa-8b2b-22a00ee49944"
    dummy_ref = "c8894b4f-c160-40fa-8b2b-22a00ee49945"
    invalid_key = "9a778aac-09b0-48f3-bc5b-6710a60b8c6f"
    patched_uuid4.side_effect = [
        str(UUID(enrl_id)),
        str(UUID(key)),
        str(UUID(invalid_key)),
    ]

    enrl_id = patched_uuid4()
    key = patched_uuid4()
    invalid_key = patched_uuid4()
    tp_ref = 534
    pl = {}
    enrolment = Enrolment(
        created=datetime.now(),
        enrolment_id=enrl_id,
        shared_secret=key,
        internal_reference=dummy_ref,
    )
    enrolment_repo.get_enrolment.return_value = enrolment

    request = CallbackRequest(  # Send invalid key which doesn't match
        enrolment_id=enrl_id,
        key=invalid_key,
        tp_sequence=tp_ref,
        payload=pl,
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_not_called()
    assert response.type == FailureType.RESOURCE_ERROR
    assert response.message == "'shared_secret' key doesn't match"
