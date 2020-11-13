from unittest import mock

from fastapi.testclient import TestClient

from app.domain.entities.callback import Callback
from app.main import app
from app.responses import FailureType, ResponseFailure, ResponseSuccess, SuccessType
from tests.test_data.callback_data_provider import CallbackDataProvider

test_data = CallbackDataProvider()
client = TestClient(app)


@mock.patch("app.use_cases.create_new_callback.CreateNewCallback")
def test_create_callback_success_created(use_case):
    code = SuccessType.CREATED
    message = "The callback has been saved."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_callback,
        type=code,
        message=message,
    )

    data = test_data.sample_callback_request
    response = client.post("/callbacks", data=data.json())
    json_result = response.json()
    callback = Callback(**json_result.get("value"))

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.CREATED.value
    assert callback == test_data.sample_callback
    assert json_result.get("message") == message


@mock.patch("app.use_cases.create_new_callback.CreateNewCallback")
def test_create_callback_success(use_case):
    message = "The callback has been fetched from the server."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_callback,
        message=message,
    )

    data = test_data.sample_callback_request
    response = client.post("/callbacks", data=data.json())
    json_result = response.json()
    callback = Callback(**json_result.get("value"))

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.SUCCESS.value
    assert callback == test_data.sample_callback
    assert json_result.get("message") == message


@mock.patch("app.use_cases.create_new_callback.CreateNewCallback")
def test_create_callback_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    data = test_data.sample_callback_request
    response = client.post("/callbacks", data=data.json())

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": message}
