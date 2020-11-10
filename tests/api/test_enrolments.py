from unittest import mock

from fastapi.testclient import TestClient

from app.domain.entities.enrolment import Enrolment
from app.main import app
from app.responses import FailureType, ResponseFailure, ResponseSuccess, SuccessType
from tests.test_data.callback_provider import CallbackDataProvider
from tests.test_data.enrolment_data_provider import DataProvider

test_data = CallbackDataProvider()
test_data_2 = DataProvider()
client = TestClient(app)


@mock.patch("app.use_cases.create_new_enrolment.CreateNewEnrolment")
def test_create_enrolment_success_created(use_case):
    code = SuccessType.CREATED
    message = "The enrolment has been created."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_enrolment,
        type=code,
        message=message,
    )

    data = test_data.sample_enrolment_request
    response = client.post("/enrolments", data=data.json())
    json_result = response.json()
    enrolment = Enrolment(**json_result.get("value"))

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.CREATED.value
    assert enrolment == test_data.sample_enrolment
    assert json_result.get("message") == message


@mock.patch("app.use_cases.create_new_enrolment.CreateNewEnrolment")
def test_create_enrolment_success(use_case):
    message = "The callback has been fetched from the server."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_enrolment,
        message=message,
    )

    data = test_data.sample_enrolment_request
    response = client.post("/enrolments", data=data.json())
    json_result = response.json()
    enrolment = Enrolment(**json_result.get("value"))

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.SUCCESS.value
    assert enrolment == test_data.sample_enrolment
    assert json_result.get("message") == message


@mock.patch("app.use_cases.create_new_enrolment.CreateNewEnrolment")
def test_create_enrolment_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    data = test_data.sample_enrolment_request
    response = client.post("/enrolments", data=data.json())

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": message}


@mock.patch("app.use_cases.get_enrolment.GetEnrolmentByID")
def test_get_enrolment_by_id_success_created(use_case):
    code = SuccessType.CREATED
    message = "The enrolment has been created."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_enrolment,
        type=code,
        message=message,
    )

    data = test_data.enrolment_id
    response = client.get(f"/enrolments/{test_data.enrolment_id}")
    json_result = response.json()
    enrolment = Enrolment(**json_result.get("value"))

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.CREATED.value
    assert enrolment == test_data.sample_enrolment
    assert json_result.get("message") == message


@mock.patch("app.use_cases.get_enrolment.GetEnrolmentByID")
def test_get_enrolment_by_id_success(use_case):
    message = "The callback has been fetched from the server."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_enrolment,
        message=message,
    )

    data = test_data.enrolment_id
    response = client.get(f"/enrolments/{test_data.enrolment_id}")
    json_result = response.json()
    enrolment = Enrolment(**json_result.get("value"))

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.SUCCESS.value
    assert enrolment == test_data.sample_enrolment
    assert json_result.get("message") == message


@mock.patch("app.use_cases.get_enrolment.GetEnrolmentByID")
def test_get_enrolment_by_id_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    response = client.get(f"/enrolments/{test_data.enrolment_id}")

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": message}


@mock.patch("app.use_cases.get_enrolment_status.GetEnrolmentStatus")
def test_get_enrolment_status_success_created(use_case):
    code = SuccessType.CREATED
    message = "The enrolment has been created."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_enrolment,
        type=code,
        message=message,
    )

    data = test_data.enrolment_id
    response = client.get(f"/enrolments/{test_data.enrolment_id}/status")
    json_result = response.json()
    enrolment = Enrolment(**json_result.get("value"))

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.CREATED.value
    assert enrolment == test_data.sample_enrolment
    assert json_result.get("message") == message


@mock.patch("app.use_cases.get_enrolment_status.GetEnrolmentStatus")
def test_get_enrolment_status_success(use_case):
    message = "The callback has been fetched from the server."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_enrolment,
        message=message,
    )

    data = test_data.enrolment_id
    response = client.get(f"/enrolments/{test_data.enrolment_id}/status")
    json_result = response.json()
    enrolment = Enrolment(**json_result.get("value"))

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.SUCCESS.value
    assert enrolment == test_data.sample_enrolment
    assert json_result.get("message") == message


@mock.patch("app.use_cases.get_enrolment_status.GetEnrolmentStatus")
def test_get_enrolment_status_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    response = client.get(f"/enrolments/{test_data.enrolment_id}/status")

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": message}


@mock.patch("app.use_cases.get_callbacks_list.GetCallbacksList")
def test_get_callbacks_list_for_enrolment_success_created(use_case):
    code = SuccessType.CREATED
    message = "The enrolment has been created."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data_2.callbacks_list1,
        type=code,
        message=message,
    )

    data = test_data.enrolment_id
    response = client.get(f"/enrolments/{test_data.enrolment_id}/journal")
    json_result = response.json()

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.CREATED.value
    assert json_result.get("value") == test_data_2.callbacks_list1_json
    assert json_result.get("message") == message


@mock.patch("app.use_cases.get_callbacks_list.GetCallbacksList")
def test_get_callbacks_list_for_enrolment_success(use_case):
    message = "The callback has been fetched from the server."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data_2.callbacks_list1,
        message=message,
    )

    data = test_data.enrolment_id
    response = client.get(f"/enrolments/{test_data.enrolment_id}/journal")
    json_result = response.json()

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.SUCCESS.value
    assert json_result.get("value") == test_data_2.callbacks_list1_json
    assert json_result.get("message") == message


@mock.patch("app.use_cases.get_callbacks_list.GetCallbacksList")
def test_get_callbacks_list_for_enrolment_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    response = client.get(f"/enrolments/{test_data.enrolment_id}/journal")

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": message}
