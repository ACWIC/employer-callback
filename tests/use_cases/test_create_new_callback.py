"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock
from uuid import uuid4

from app.repositories.callback_repo import CallbackRepo
from app.repositories.enrolment_repo import EnrolmentRepo
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.responses import FailureType, ResponseFailure, SuccessType
from app.use_cases.create_new_callback import CreateNewCallback
from tests.domain.entities import factories as entities_factories
from tests.requests import factories as requests_factories


def test_create_new_callback_success():
    """
    Ensure that creating a new callback with CreateNewCallback
    use case produces a valid response.
    """
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)
    enrolment = entities_factories.enrolment()
    enrolment_repo.get_enrolment.return_value = enrolment
    request = requests_factories.callback_request(
        enrolment_id=enrolment.enrolment_id, shared_secret=enrolment.shared_secret
    )
    callback = entities_factories.callback_event_from_request(request=request)
    repo.save_callback.return_value = callback

    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    assert response.type == SuccessType.SUCCESS
    assert response.message == "The callback has been saved."
    assert response.value.get("enrolment_id") == enrolment.enrolment_id
    assert response.value.get("shared_secret") == enrolment.shared_secret


def test_create_new_callback_failure():
    """
    When creating a new enrollment authorization,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment = entities_factories.enrolment()
    enrolment_repo.get_enrolment.return_value = enrolment
    repo.save_callback.side_effect = Exception()

    request = requests_factories.callback_request(
        enrolment_id=enrolment.enrolment_id, shared_secret=enrolment.shared_secret
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

    invalid_enrolment_id = str(uuid4())
    request = requests_factories.callback_request(
        enrolment_id=invalid_enrolment_id,
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_not_called()
    assert response.type == FailureType.RESOURCE_ERROR
    assert response.message == error_message


def test_create_new_callback_failure_on_invalid_shared_secret():
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)

    enrolment = entities_factories.enrolment()
    enrolment_repo.get_enrolment.return_value = enrolment

    invalid_shared_secret = str(uuid4())
    request = requests_factories.callback_request(
        shared_secret=invalid_shared_secret,
    )
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_not_called()
    assert response.type == FailureType.UNAUTHORISED_ERROR
    assert response.message == "'shared_secret' key doesn't match"
