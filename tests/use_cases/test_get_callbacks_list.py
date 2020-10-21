from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock, patch
from uuid import UUID

from app.config import settings
from app.repositories.callback_repo import CallbackRepo
from app.repositories.s3_callback_repo import S3CallbackRepo
from app.responses import FailureType, SuccessType
from app.use_cases.get_callbacks_list import GetCallbacksList
from tests.test_data.callback_provider import CallbackDataProvider


def test_get_callbacks_list_success():
    repo = mock.Mock(spec=CallbackRepo)
    callback = CallbackDataProvider().sample_callback

    repo.get_callbacks_list.return_value = (
        CallbackDataProvider().sample_get_callback_list
    )
    use_case = GetCallbacksList(callback_repo=repo)
    response = use_case.execute(CallbackDataProvider().enrolment_id)

    assert response.type == SuccessType.SUCCESS
    assert "callbacks_list" in response.value
    assert response.value["callbacks_list"][0] == callback


def test_get_callbacks_list_failure():
    repo = mock.Mock(spec=CallbackRepo)
    repo.get_callbacks_list.side_effect = Exception()
    use_case = GetCallbacksList(callback_repo=repo)
    response = use_case.execute(CallbackDataProvider().enrolment_id)

    assert response.type == FailureType.RESOURCE_ERROR


@patch("app.repositories.s3_enrolment_repo.S3EnrolmentRepo.get_enrolment")
@patch("uuid.uuid4")
@patch("boto3.client")
def test_get_callbacks_list(boto_client, uuid4, repo_get_enrolment):
    """
    Ensure the S3Enrolmentrepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    enrolment_id = "look-at-my-enrolment-id"
    fixed_uuid_str = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    uuid4.return_value = UUID(fixed_uuid_str)
    repo = S3CallbackRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"
    settings.CALLBACK_BUCKET = "some-bucket1"
    repo_get_enrolment.return_value = True

    with patch(
        "json.loads",
        MagicMock(
            side_effect=[
                {
                    "callback_id": "1c1e9bd1-82ed-42a6-a82b-11fdacecc2db",
                    "received": "2020-10-11T16:06:53.739338",
                    "enrolment_id": "cdf727e1-d9be-4450-9e64-8f18916598df",
                    "shared_secret": "04159571-6fa2-4d67-862a-ca9335372b03",
                    "tp_sequence": 0,
                    "payload": {},
                }
            ]
        ),
    ):
        boto_client.return_value.list_objects = list_objects_sample_content
        callbacks_list = repo.get_callbacks_list(enrolment_id=enrolment_id)
        print("test callbacks_list", callbacks_list)

    assert callbacks_list == {
        "callbacks_list": [
            {
                "callback_id": "1c1e9bd1-82ed-42a6-a82b-11fdacecc2db",
                "received": datetime(2020, 10, 11, 16, 6, 53, 739338),
            }
        ]
    }

    boto_client.return_value.get_object.assert_called_once_with(
        Key=f"{enrolment_id}.json", Bucket="some-bucket1"
    )


def list_objects_sample_content(Bucket, Prefix):
    return {
        "Contents": [
            {
                "callback_id": "1c1e9bd1-82ed-42a6-a82b-11fdacecc2db",
                "bucket": Bucket,
                "prefix": Prefix,
                "Key": "look-at-my-enrolment-id.json",
            }
        ]
    }
