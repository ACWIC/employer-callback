import base64
import unittest

import pytest
from botocore.exceptions import BotoCoreError, ClientError, ParamValidationError

from app.utils.error_handling import (
    CustomBase64Exception,
    S3Exception,
    handle_base64_errors,
    handle_s3_errors,
)


class TestS3Errors(unittest.TestCase):
    def test_client_error(self):
        error_response = {"Error": {"Code": "123", "Message": "Test Message"}}
        with pytest.raises(S3Exception) as exception:
            with handle_s3_errors():
                raise ClientError(error_response=error_response, operation_name="TEST")

        assert (
            str(exception.value)
            == "Client Error!\nPlease check the error code and message below.\nCode: 123\nMessage: Test Message"
        )

    def test_no_such_key_error(self):
        error_response = {"Error": {"Code": "NoSuchKey", "Message": ""}}
        with pytest.raises(S3Exception) as exception:
            with handle_s3_errors():
                raise ClientError(error_response=error_response, operation_name="TEST")

        assert (
            str(exception.value)
            == "Object with the specified key doesn't exist in the bucket."
        )

    def test_parameter_validation_error(self):
        with pytest.raises(ValueError) as exception:
            with handle_s3_errors():
                raise ParamValidationError(report="Test")

        assert (
            str(exception.value)
            == "The parameters you provided are incorrect: Parameter validation failed:\nTest"
        )

    def test_botocore_error(self):
        with pytest.raises(S3Exception) as exception:
            with handle_s3_errors():
                raise BotoCoreError(msg="TEST")

        assert (
            str(exception.value)
            == "BotoCoreError! Please check the error message: An unspecified error occurred"
        )

    def test_unknown_error(self):
        with pytest.raises(Exception) as exception:
            with handle_s3_errors():
                raise Exception("Random Error")

        assert (
            str(exception.value)
            == "Unknown Error! This might be a Python Error.\nPlease check the error message: Random Error"
        )


class TestEncodeDecodeErrors(unittest.TestCase):
    def test_type_error(self):
        with pytest.raises(CustomBase64Exception) as exception:
            with handle_base64_errors():
                base64.urlsafe_b64encode("test")

        assert (
            str(exception.value)
            == "TypeError! Please check the error message: a bytes-like object is required, not 'str'"
        )

    def test_unknown_error(self):
        with pytest.raises(Exception) as exception:
            with handle_base64_errors():
                raise Exception("Random Error")

        assert (
            str(exception.value)
            == "Unknown Error! Please check the error message: Random Error"
        )
