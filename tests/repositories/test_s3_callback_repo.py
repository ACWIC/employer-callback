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
from app.repositories.s3_callback_repo import S3CallbackRepo


@patch('boto3.client')
def test_s3_initialisation(boto_client):
    """
    Ensure the S3Enrolmentrepo makes a boto3 connection.
    """
    S3CallbackRepo()
    boto_client.assert_called_once()


@patch('uuid.uuid4')
@patch('boto3.client')
def test_save_callback(boto_client, uuid4):
    """
    Ensure the S3CallbackRepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    callback_id = UUID('1dad3dd8-af28-4e61-ae23-4c93a456d10e')
    uuid4.return_value = callback_id
    enrolment_id = 'the_employer_generated_this_identifier'
    key = 'the_employer_generated_this_secret'

    repo = S3CallbackRepo()
    environ['CALLBACK_BUCKET'] = 'some-bucket'
    callback = repo.save_callback(enrolment_id, key)

    # TODO: assert enrollment is of the appropriate domain model type
    assert callback.callback_id == callback_id
    assert str(callback_id) == '1dad3dd8-af28-4e61-ae23-4c93a456d10e'

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(callback.json(), 'utf-8'),
        Key=f'{callback.enrolment_id}/{callback.callback_id}.json',  # NOQA
        Bucket='some-bucket'
    )
