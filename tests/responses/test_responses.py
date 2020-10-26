from app.responses import FailureType, ResponseFailure, ResponseSuccess, SuccessType


def test_response_failure_type():
    response = ResponseFailure(type=FailureType.SYSTEM_ERROR, message="")
    assert bool(response) is False


def test_response_success_type():
    response = ResponseSuccess(value={})
    assert bool(response) is True


def test_response_failure_build_from_system_error():
    response = ResponseFailure.build_from_system_error(message="system error test")
    assert response.type == FailureType.SYSTEM_ERROR


def test_response_failure_build_from_resource_error():
    response = ResponseFailure.build_from_resource_error(message="resource error test")
    assert response.type == FailureType.RESOURCE_ERROR


def test_response_failure_build_from_validation_error():
    response = ResponseFailure.build_from_validation_error(
        message="validation error test"
    )
    assert response.type == FailureType.VALIDATION_ERROR


def test_response_failure_build_from_unauthorised_error():
    response = ResponseFailure.build_from_unauthorised_error(
        message="unauthorised error test"
    )
    assert response.type == FailureType.UNAUTHORISED_ERROR


def test_response_success_build():
    response = ResponseSuccess(
        value={"test": "123"}, type=SuccessType.SUCCESS.value, message=""
    )
    json_response = response.build()
    assert b'{"value":{"test":"123"}' in json_response.body
    assert json_response.status_code == SuccessType.SUCCESS.value
