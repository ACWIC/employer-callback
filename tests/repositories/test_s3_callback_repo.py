"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from os import environ
from unittest.mock import patch

from app.config import settings
from app.repositories.s3_callback_repo import S3CallbackRepo
from app.requests.callback_requests import CallbackRequest


@patch("boto3.client")
def test_s3_initialisation(boto_client):
    """
    Ensure the S3Enrolmentrepo makes a boto3 connection.
    """
    S3CallbackRepo()
    boto_client.assert_called_once()


@patch("boto3.client")
def test_save_callback(boto_client):
    """
    Ensure the S3CallbackRepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    repo = S3CallbackRepo()
    environ["CALLBACK_BUCKET"] = "some-bucket"

    request = CallbackRequest(
        **{
            "sender_sequence": 9876543,
            "shared_secret": "the_employer_generated_this_secret",
            "message_type_version": "v1",
            "enrolment_id": "the_employer_generated_this_identifier",
            "structured_data": {"key": "value", "another_key": "another value"},
            "attachments": [{"name": "dummy.txt", "content": b"empty"}],
        }
    )
    callback = repo.save_callback(request)

    # TODO: assert enrollment is of the appropriate domain model type

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(callback.json(), "utf-8"),
        Key=f"callbacks/{callback.enrolment_id}/{callback.callback_id}.json",  # NOQA
        Bucket=settings.CALLBACK_BUCKET,
    )
