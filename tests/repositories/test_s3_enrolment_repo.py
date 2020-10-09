"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from os import environ
from unittest.mock import patch
from uuid import UUID

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo


@patch("boto3.client")
def test_s3_initialisation(boto_client):
    """
    Ensure the S3Enrolmentrepo makes a boto3 connection.
    """
    S3EnrolmentRepo()
    boto_client.assert_called_once()


@patch("uuid.uuid4")
@patch("boto3.client")
def test_save_enrolment(boto_client, uuid4):
    """
    Ensure the S3Enrolmentrepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    fixed_uuid_str = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    uuid4.return_value = UUID(fixed_uuid_str)
    repo = S3EnrolmentRepo()
    environ["ENROLMENT_BUCKET"] = "some-bucket"
    enrolment = repo.save_enrolment(enrolment_id="look-at-my-enrolment-id")

    # TODO: mock datetime.datetime.now and assert that too
    assert str(enrolment.enrolment_id) == "look-at-my-enrolment-id"
    assert str(enrolment.key) == fixed_uuid_str

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(enrolment.json(), "utf-8"),
        Key=f"{enrolment.enrolment_id}.json",  # NOQA
        Bucket="some-bucket",
    )


def test_get_enrolment():
    """
    Ensure the S3Enrolmentrepo returns an object with OK data
    """
    """"""
