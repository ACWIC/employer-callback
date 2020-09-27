"""
These tests evaluate (and document) the business logic.
"""
from uuid import uuid4
from unittest import mock
from app.domain.entities.callback import Callback
from app.repositories.callback_repo import CallbackRepo
from app.requests.callback_requests import NewCallbackRequest
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

    callback = Callback(
        callback_id=cb_id,
        enrolment_id=enrl_id,
        key=key
    )
    repo.save_callback.return_value = callback

    request = NewCallbackRequest(
        enrolment_id=enrl_id,
        key=key
    )
    use_case = CreateNewCallback(callback_repo=repo)
    response = use_case.execute(request)

    assert response.type == 'Success'


def test_create_new_callback_failure():
    """
    When creating a new enrollment authorisation,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=CallbackRepo)
    enrl_id = 'dummy_enrolment_id'
    key = 'dummy_enrolment_key'

    repo.save_callback.side_effect = Exception()
    request = NewCallbackRequest(
        enrolment_id=enrl_id,
        key=key
    )
    use_case = CreateNewCallback(callback_repo=repo)
    response = use_case.execute(request)

    assert response.type == 'ResourceError'
