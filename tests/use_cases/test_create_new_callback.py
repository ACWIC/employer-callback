"""
These tests evaluate (and document) the business logic.
"""
from datetime import datetime
import random
from uuid import uuid4
from unittest import mock
from app.domain.entities.callback import Callback
from app.repositories.callback_repo import CallbackRepo
from app.requests.callback_requests import CallbackRequest
from app.responses import FailureType, SuccessType
from app.use_cases.create_new_callback import CreateNewCallback


def test_create_new_callback_success():
    """
    When creating a new enrollment authorisation,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=CallbackRepo)
    # dummy data
    cb_id = uuid4()
    enrl_id = 'dummy_enrolment_id'
    key = 'dummy_enrolment_key'
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
    repo.save_callback.return_value = callback

    request = CallbackRequest(
        enrolment_id=enrl_id,
        key=key,
        tp_sequence=tp_ref,
        payload=pl,
        invalid=invalid,
    )
    use_case = CreateNewCallback(callback_repo=repo)
    response = use_case.execute(request)

    assert response.status_code == SuccessType.SUCCESS


def test_create_new_callback_failure():
    """
    When creating a new enrollment authorisation,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=CallbackRepo)
    enrl_id = 'dummy_enrolment_id'
    key = 'dummy_enrolment_key'
    tp_ref = 534
    pl = {"brace": "yourself"}
    invalid = {}
    repo.save_callback.side_effect = Exception()

    request = CallbackRequest(
        enrolment_id=enrl_id,
        key=key,
        tp_sequence=tp_ref,
        payload=pl,
        invalid=invalid,
    )
    use_case = CreateNewCallback(callback_repo=repo)
    response = use_case.execute(request)

    assert response.status_code == FailureType.RESOURCE_ERROR


def test_create_new_callback_failure_on_invalid_enrolment_id():
    repo = mock.Mock(spec=CallbackRepo)
    invalid_enrl_id = 123456789
    key = 'shared_secret_key'
    tp_ref = 534
    pl = {}
    invalid = {}
    # repo.save_callback.side_effect = Exception("'enrolment_id' doesn't exist!")

    request = CallbackRequest(
        enrolment_id=invalid_enrl_id,
        key=key,
        tp_sequence=tp_ref,
        payload=pl,
        invalid=invalid,
    )
    use_case = CreateNewCallback(callback_repo=repo)
    response = use_case.execute(request)

    assert response.status_code == FailureType.RESOURCE_ERROR
    assert response.message == "Exception: Resource Error! 'enrolment_id' doesn't exist!"


def test_create_new_callback_failure_on_invalid_shared_secret():
    repo = mock.Mock(spec=CallbackRepo)
    invalid_enrl_id = "dummy_enrolment_id"
    key = 'INVALID_SECRET_KEY'
    tp_ref = 534
    pl = {}
    invalid = {}
    repo.save_callback.side_effect = Exception()

    request = CallbackRequest(
        enrolment_id=invalid_enrl_id,
        key=key,
        tp_sequence=tp_ref,
        payload=pl,
        invalid=invalid,
    )
    use_case = CreateNewCallback(callback_repo=repo)
    response = use_case.execute(request)

    assert response.status_code == FailureType.RESOURCE_ERROR
    assert response.message == "Exception: Resource Error! 'shared_secret' doesn't match"
