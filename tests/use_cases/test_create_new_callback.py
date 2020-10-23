"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock

from botocore.exceptions import ClientError

from app.repositories.callback_repo import CallbackRepo
from app.repositories.enrolment_repo import EnrolmentRepo
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.responses import FailureType, ResponseFailure, SuccessType
from app.use_cases.create_new_callback import CreateNewCallback
from tests.test_data.callback_provider import CallbackDataProvider

test_data = CallbackDataProvider()


def test_create_new_callback_success():
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)
    callback = test_data.sample_callback
    enrolment = test_data.sample_enrolment
    enrolment_repo.get_enrolment.return_value = enrolment
    repo.save_callback.return_value = (True, callback)

    request = test_data.sample_callback_request
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    assert response.type == SuccessType.CREATED
    assert response.message == "The callback has been saved."
    assert response.value.get("enrolment_id") == enrolment.enrolment_id
    assert response.value.get("shared_secret") == enrolment.shared_secret


def test_create_new_callback_idempotence():
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)
    callback = test_data.sample_callback
    enrolment = test_data.sample_enrolment
    enrolment_repo.get_enrolment.return_value = enrolment
    repo.save_callback.side_effect = [(True, callback), (False, callback)]

    request = test_data.sample_callback_request
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    # Try to save same callback twice
    use_case.execute(request)
    response = use_case.execute(request)

    assert response.type == SuccessType.SUCCESS
    assert response.message == "The callback has been fetched from the server."
    assert response.value.get("callback_id") == test_data.callback_id
    assert response.value.get("enrolment_id") == enrolment.enrolment_id
    assert response.value.get("shared_secret") == enrolment.shared_secret
    assert response.value.get("received") == test_data.received


def test_create_new_callback_failure():
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment = test_data.sample_enrolment
    enrolment_repo.get_enrolment.return_value = enrolment
    repo.save_callback.side_effect = Exception()

    request = test_data.sample_callback_request
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_called_once()
    assert response.type == FailureType.RESOURCE_ERROR


def test_create_new_callback_failure_on_invalid_enrolment_id():
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)

    error_response = {"Code": "NoSuchKey"}
    error_message = ClientError(error_response=error_response, operation_name="TEST")
    enrolment_repo.get_enrolment.side_effect = error_message

    request = test_data.sample_callback_request
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_not_called()
    assert response.type == FailureType.RESOURCE_ERROR
    expected_message = ResponseFailure.build_from_resource_error(
        message=error_message
    ).message
    assert response.message == expected_message


def test_create_new_callback_failure_on_invalid_shared_secret():
    repo = mock.Mock(spec=CallbackRepo)
    enrolment_repo = mock.Mock(spec=EnrolmentRepo)

    enrolment = test_data.sample_enrolment
    enrolment_repo.get_enrolment.return_value = enrolment

    request = test_data.sample_invalid_callback_request
    use_case = CreateNewCallback(callback_repo=repo, enrolment_repo=enrolment_repo)
    response = use_case.execute(request)

    repo.save_callback.assert_not_called()
    assert response.type == FailureType.UNAUTHORISED_ERROR
    assert response.message == "'shared_secret' key doesn't match"
