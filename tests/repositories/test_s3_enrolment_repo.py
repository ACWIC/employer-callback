"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import UUID

from app.config import settings
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.utils import Random


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
    settings.ENROLMENT_BUCKET = "some-bucket"
    enrolment_id = Random.get_uuid()
    enrolment = {
        "enrolment_id": enrolment_id,
        "shared_secret": Random.get_uuid(),
        "internal_reference": fixed_uuid_str,
        "created": datetime.now(),
    }

    enrolment = repo.save_enrolment(enrolment)

    # TODO: mock datetime.datetime.now and assert that too
    assert str(enrolment.enrolment_id) == enrolment_id
    assert str(enrolment.internal_reference) == fixed_uuid_str

    enrolment_hash = Random.get_str_hash(enrolment.internal_reference)
    boto_client.return_value.put_object(
        Body=bytes(enrolment.json(), "utf-8"),
        Key=f"employer_reference/{enrolment_hash}/enrolment_id.json",  # NOQA
        Bucket="some-bucket",
    )
    assert boto_client.return_value.put_object.call_count == 3


@patch("uuid.uuid4")
@patch("boto3.client")
def test_get_enrolment(boto_client, uuid4):
    """
    Ensure the S3Enrolmentrepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    print("test_get_enrolment()")
    fixed_uuid_str = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    fixed_uuid_str_ = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    uuid4.return_value = UUID(fixed_uuid_str)
    repo = S3EnrolmentRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"
    with patch(
        "json.loads",
        MagicMock(
            side_effect=[
                {
                    "enrolment_id": "look-at-my-enrolment-id",
                    "shared_secret": fixed_uuid_str,
                    "internal_reference": fixed_uuid_str_,
                    "created": "2020-10-07 15:37:16.727308",
                }
            ]
        ),
    ):
        enrolment = repo.get_enrolment(enrolment_id="look-at-my-enrolment-id")
        print("enrolment", enrolment, type(enrolment))

    print(str(enrolment.created), "2020-10-07 15:37:16.727308")
    assert str(enrolment.created) == "2020-10-07 15:37:16.727308"
    assert str(enrolment.enrolment_id) == "look-at-my-enrolment-id"
    assert str(enrolment.shared_secret) == fixed_uuid_str
    assert str(enrolment.internal_reference) == fixed_uuid_str_

    boto_client.return_value.get_object.assert_called_once_with(
        Key=f"enrolments/{enrolment.enrolment_id}.json", Bucket="some-bucket"  # NOQA
    )


@patch("app.repositories.s3_callback_repo.S3CallbackRepo.get_callbacks_list")
@patch("uuid.uuid4")
@patch("boto3.client")
def test_get_enrolment_status(boto_client, uuid4, callback_repo_list):
    """
    Ensure the S3Enrolmentrepo returns an object with OK data
    and that get_enrolment_status returns appropriate object.
    """
    repo = S3EnrolmentRepo()
    # settings.ENROLMENT_BUCKET = "some-bucket"
    callback_id = Random.get_uuid()
    callback_id_2 = Random.get_uuid()

    callback_received = "2020-10-07 15:37:16.727308"
    callback_received_2 = "2020-10-07 16:37:16.727308"

    callback_repo_list.return_value = {
        "callbacks_list": [
            {"callback_id": callback_id, "received": callback_received},
            {"callback_id": callback_id_2, "received": callback_received_2},
        ]
    }

    enrolment_status = repo.get_enrolment_status(
        enrolment_id="look-at-my-enrolment-id"
    )["status"]
    print("enrolment_status", enrolment_status, type(enrolment_status))

    assert str(enrolment_status["most_recent_callback"]) == "2020-10-07 16:37:16.727308"
    assert str(enrolment_status["total_callbacks"]) == "2"

    callback_repo_list.assert_called_once_with("look-at-my-enrolment-id")  # NOQA

    callback_repo_list.return_value = {"callbacks_list": []}

    enrolment_status = repo.get_enrolment_status(
        enrolment_id="look-at-my-enrolment-id"
    )["status"]

    print("enrolment_status", enrolment_status, type(enrolment_status))
    assert str(enrolment_status["most_recent_callback"]) == ""
    assert str(enrolment_status["total_callbacks"]) == "0"
