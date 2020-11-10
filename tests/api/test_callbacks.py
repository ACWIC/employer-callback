from unittest import mock

from fastapi.testclient import TestClient

from app.domain.entities.callback import Callback
from app.main import app
from app.responses import ResponseSuccess, SuccessType
from tests.test_data.callback_provider import CallbackDataProvider

test_data = CallbackDataProvider()
client = TestClient(app)


@mock.patch("app.use_cases.create_new_callback.CreateNewCallback")
def test_create_callbacks(use_case):
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
