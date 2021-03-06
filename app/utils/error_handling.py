from contextlib import contextmanager

from botocore.exceptions import BotoCoreError, ClientError, ParamValidationError


class S3Exception(Exception):
    pass


class CustomBase64Exception(Exception):
    pass


@contextmanager
def handle_s3_errors():
    try:
        yield
    except ClientError as error:
        if error.response["Error"]["Code"] == "NoSuchKey":
            raise S3Exception(
                "Object with the specified key doesn't exist in the bucket."
            )
        else:
            raise S3Exception(
                f"Client Error!\nPlease check the error code and message below."
                f"\nCode: {error.response['Error']['Code']}"
                f"\nMessage: {error.response['Error']['Message']}"
            )
    except ParamValidationError as error:
        raise ValueError(f"The parameters you provided are incorrect: {error}")
    except Exception as exception:
        if not isinstance(exception, BotoCoreError):
            raise Exception(
                f"Unknown Error! This might be a Python Error.\n"
                f"Please check the error message: {exception}"
            )
        else:
            raise S3Exception(
                f"BotoCoreError! Please check the error message: {exception}"
            )


@contextmanager
def handle_base64_errors():
    try:
        yield
    except TypeError as error:
        raise CustomBase64Exception(
            f"TypeError! Please check the error message: {error}"
        )
    except SyntaxError as error:
        raise CustomBase64Exception(
            f"SyntaxError! Please check the error message: {error}"
        )  # noqa - pytest raises error during the test collection
    except Exception as exception:
        raise Exception(f"Unknown Error! Please check the error message: {exception}")
