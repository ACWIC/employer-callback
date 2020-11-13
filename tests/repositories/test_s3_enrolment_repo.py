"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from unittest import mock

from app.config import settings
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from tests.test_data.callback_data_provider import CallbackDataProvider

test_data = CallbackDataProvider()


@mock.patch("boto3.client")
def test_s3_initialisation(boto_client):
    """
    Ensure the S3Enrolmentrepo makes a boto3 connection.
    """
    S3EnrolmentRepo()
    boto_client.assert_called_once()


@mock.patch("json.loads")
@mock.patch("boto3.client")
def test_get_enrolment(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"

    enrolment_id = test_data.enrolment_id
    sample_enrolment = test_data.sample_enrolment

    json_loads.return_value = sample_enrolment.dict()
    enrolment = repo.get_enrolment(enrolment_id)

    assert enrolment == sample_enrolment
    boto_client.return_value.get_object.assert_called_once_with(
        Key="enrolments/" + enrolment_id + ".json",
        Bucket=settings.ENROLMENT_BUCKET,
    )
