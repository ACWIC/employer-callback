"""
These tests evaluate (and document) the business logic.
"""
from datetime import datetime
import random
from uuid import uuid4
from unittest import mock
from app.domain.entities.callback import Callback
from app.domain.entities.enrolment import Enrolment
from app.repositories.callback_repo import CallbackRepo
from app.repositories.enrolment_repo import EnrolmentRepo
from app.requests.callback_requests import CallbackRequest
from app.responses import FailureType, SuccessType
from app.use_cases.create_new_callback import CreateNewCallback


def test_create_new_callback_success():
    """
    When creating a new enrollment authorisation,
    if everything goes according to plan,
    the response type should be "Success".
    """
    callback_repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)

    # dummy data
    cb_id = uuid4()
    enrl_id = uuid4()
    key = uuid4()
    tp_ref = random.randint(0, 99999)
    rx = datetime.now()
    pl = {"data": "blbnjsd;fnbs"}
    invalid = {}
    callback = Callback(
        callback_id=cb_id,
        enrolment_id=enrl_id,
        key=key,
        tp_sequence=tp_ref,
        received=rx,
        payload=pl
    )
    enrolment = Enrolment(
        enrolment_id=enrl_id,
        key=key,
    )
    callback_repo.save_callback.return_value = callback
    enrolment_repo.get_enrolment_by_id.return_value = enrolment

    request = CallbackRequest(
        enrolment_id=enrl_id,
        key=key,
        tp_sequence=tp_ref,
        payload=pl,
        invalid=invalid,
    )
    use_case = CreateNewCallback(callback_repo=callback_repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    assert response.status_code == SuccessType.SUCCESS


def test_create_new_callback_failure():
    """
    When creating a new enrollment authorisation,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    callback_repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)

    # dummy data
    cb_id = uuid4()
    enrl_id = uuid4()
    key = uuid4()
    tp_ref = 534
    pl = {"brace": "yourself"}
    enrolment = Enrolment(
        enrolment_id=enrl_id,
        key=key,
    )
    enrolment_repo.get_enrolment_by_id.return_value = enrolment
    callback_repo.save_callback.side_effect = Exception()

    request = CallbackRequest(
        enrolment_id=enrl_id,
        key=key,
        tp_sequence=tp_ref,
        payload=pl,
    )
    use_case = CreateNewCallback(callback_repo=callback_repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    assert response.status_code == FailureType.RESOURCE_ERROR


def test_create_new_callback_failure_on_invalid_enrolment_id():
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)
    enrl_id = uuid4()
    invalid_enrl_id = uuid4()
    key = uuid4()
    tp_ref = 534
    pl = {}
    enrolment_repo.get_enrolment_by_id.side_effect = None

    request = CallbackRequest(
        enrolment_id=enrl_id,
        key=key,
        tp_sequence=tp_ref,
        payload=pl,
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    assert response.status_code == FailureType.RESOURCE_ERROR
    assert response.message == "'enrolment_id' doesn't exist!"


def test_create_new_callback_failure_on_invalid_shared_secret():
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)
    enrl_id = uuid4()
    key = uuid4()
    invalid_key = uuid4()
    tp_ref = 534
    pl = {}
    enrolment = Enrolment(
        enrolment_id=enrl_id,  # Use the correct key for enrolment id
        key=invalid_key,
    )
    enrolment_repo.get_enrolment_by_id.side_effect = enrolment

    request = CallbackRequest(
        enrolment_id=enrl_id,
        key=key,
        tp_sequence=tp_ref,
        payload=pl,
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    assert response.status_code == FailureType.RESOURCE_ERROR
    assert response.message == "'shared_secret' key doesn't match"
