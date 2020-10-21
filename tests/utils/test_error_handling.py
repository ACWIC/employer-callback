import pytest
from botocore.exceptions import BotoCoreError, ClientError, ParamValidationError

from app.utils.error_handling import S3Exception, handle_s3_errors


def test_client_error():
    error_response = {"Error": {"Code": "", "Message": ""}}
    with pytest.raises(S3Exception):
        with handle_s3_errors():
            raise ClientError(error_response=error_response, operation_name="TEST")


def test_no_such_key_error():
    error_response = {"Error": {"Code": "NoSuchKey", "Message": ""}}
    with pytest.raises(S3Exception):
        with handle_s3_errors():
            raise ClientError(error_response=error_response, operation_name="TEST")


def test_parameter_validation_error():
    with pytest.raises(ValueError):
        with handle_s3_errors():
            raise ParamValidationError(report="Test")


def test_botocore_error():
    with pytest.raises(S3Exception):
        with handle_s3_errors():
            raise BotoCoreError(msg="TEST")


def test_unknown_error():
    with pytest.raises(Exception):
        with handle_s3_errors():
            raise Exception("Random Error")
