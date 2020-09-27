"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from os import environ
from uuid import UUID
from unittest.mock import patch
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo


@patch('boto3.client')
def test_s3_initialisation(boto_client):
    """
    Ensure the S3Enrolmentrepo makes a boto3 connection.
    """
    S3EnrolmentRepo()
    boto_client.assert_called_once()


@patch('uuid.uuid4')
@patch('boto3.client')
def test_save_enrolment(boto_client, uuid4):
    """
    Ensure the S3Enrolmentrepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    uuid4.return_value = UUID('1dad3dd8-af28-4e61-ae23-4c93a456d10e')
    repo = S3EnrolmentRepo()
    environ['ENROLMENT_AUTHORISATION_BUCKET'] = 'some-bucket'
    enrolment = repo.save_enrolment(course_id='123', student_id='abc')

    # TODO: assert enrollment is of the appropriate domain model type
    assert enrolment.course_id == '123'
    assert enrolment.student_id == 'abc'
    assert str(enrolment.uuid) == '1dad3dd8-af28-4e61-ae23-4c93a456d10e'

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(enrolment.json(), 'utf-8'),
        Key=f'{enrolment.uuid}.json',  # NOQA
        Bucket='some-bucket'
    )
