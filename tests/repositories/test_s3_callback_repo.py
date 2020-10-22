"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from datetime import datetime
from os import environ
from unittest.mock import patch

from app.config import settings
from app.repositories.s3_callback_repo import S3CallbackRepo


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
    callback_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    e_id = "the_employer_generated_this_identifier"
    k = "the_employer_generated_this_secret"
    tp_seq = 9876543
    pl = {"say": "what?"}
    repo = S3CallbackRepo()
    environ["CALLBACK_BUCKET"] = "some-bucket"

    params = {
        "callback_id": callback_id,
        "enrolment_id": e_id,
        "shared_secret": k,
        "tp_sequence": tp_seq,
        "payload": pl,
        "received": datetime.now(),
    }
    is_created, callback = repo.save_callback(params)

    assert callback.callback_id == callback_id

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(callback.json(), "utf-8"),
        Key=f"callbacks/{callback.enrolment_id}/{callback.callback_id}.json",  # NOQA
        Bucket=settings.CALLBACK_BUCKET,
    )
