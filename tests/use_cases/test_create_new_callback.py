"""
These tests evaluate (and document) the business logic.
"""
import random
from datetime import datetime
from unittest import mock

from app.domain.entities.callback import Callback
from app.repositories.callback_repo import CallbackRepo
from app.requests.callback_requests import CallbackRequest
from app.use_cases.create_new_callback import CreateNewCallback


def test_create_new_callback_success():
    """
    When creating a new enrollment authorisation,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=CallbackRepo)
    # dummy data
    cb_id = "dummy_callback_id"
    enrl_id = "dummy_enrolment_id"
    shared_secret = "dummy_enrolment_key"
    tp_ref = random.randint(0, 99999)
    rx = datetime.now()
    pl = {"data": "blbnjsd;fnbs"}
    callback = Callback(
        callback_id=cb_id,
        enrolment_id=enrl_id,
        shared_secret=shared_secret,
        tp_sequence=tp_ref,
        received=rx,
        payload=pl,
    )
    repo.save_callback.return_value = callback

    request = CallbackRequest(
        enrolment_id=enrl_id,
        shared_secret=shared_secret,
        tp_sequence=tp_ref,
        payload=pl,
    )
    use_case = CreateNewCallback(callback_repo=repo)
    response = use_case.execute(request)

    assert response.type == "Success"


def test_create_new_callback_failure():
    """
    When creating a new enrollment authorisation,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=CallbackRepo)
    enrl_id = "dummy_enrolment_id"
    shared_secret = "dummy_enrolment_key"
    tp_ref = 534
    pl = {"brace": "yourself"}
    repo.save_callback.side_effect = Exception()

    request = CallbackRequest(
        enrolment_id=enrl_id,
        shared_secret=shared_secret,
        tp_sequence=tp_ref,
        payload=pl,
    )
    use_case = CreateNewCallback(callback_repo=repo)
    response = use_case.execute(request)

    assert response.type == "ResourceError"
