"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
import datetime
from unittest import mock

from app.config import settings
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from tests.test_data.enrolment_data_provider import DataProvider

test_data = DataProvider()


@mock.patch("boto3.client")
def test_s3_initialisation(boto_client):
    """
    Ensure the S3Enrolmentrepo makes a boto3 connection.
    """
    S3EnrolmentRepo()
    boto_client.assert_called_once()


@mock.patch("app.utils.random.Random.get_uuid")
@mock.patch("boto3.client")
def test_create_enrolment(boto_client, get_uuid):
    repo = S3EnrolmentRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"

    sample_uuid = test_data.sample_uuid
    enrolment_id = sample_uuid
    sample_enrolment = test_data.sample_create_enrolment
    internal_reference = test_data.internal_reference

    get_uuid.return_value = sample_uuid
    with mock_datetime_now(test_data.created, datetime):
        enrolment = repo.create_enrolment(internal_reference)

    assert enrolment == sample_enrolment
    boto_client.return_value.put_object.assert_called_with(
        Body=bytes(enrolment.json(), "utf-8"),
        Key=f"enrolments/{enrolment_id}.json",
        Bucket=settings.ENROLMENT_BUCKET,
    )


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


@mock.patch("json.loads")
@mock.patch("boto3.client")
def test_get_callbacks_list(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.CALLBACK_BUCKET = "some-bucket"

    enrolment_id = test_data.enrolment_id
    callback = test_data.sample_callback.dict()

    boto_client.return_value.list_objects = list_objects_sample_content
    json_loads.return_value = callback

    callbacks_list = repo.get_callbacks_list(enrolment_id)

    assert callbacks_list == test_data.callbacks_list
    boto_client.return_value.get_object.assert_called_once_with(
        Key="callbacks/" + enrolment_id + ".json",
        Bucket=settings.ENROLMENT_BUCKET,
    )


@mock.patch("json.loads")
@mock.patch("boto3.client")
def test_get_callbacks_list_empty(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.CALLBACK_BUCKET = "some-bucket"

    enrolment_id = test_data.enrolment_id
    callback = test_data.sample_callback.dict()

    boto_client.return_value.list_objects = list_objects_sample_content_empty
    json_loads.return_value = callback

    callbacks_list = repo.get_callbacks_list(enrolment_id)

    assert callbacks_list == {"callbacks_list": []}


@mock.patch("app.repositories.s3_enrolment_repo.S3EnrolmentRepo.get_callbacks_list")
def test_get_enrolment_status(get_callbacks_list):
    repo = S3EnrolmentRepo()
    settings.CALLBACK_BUCKET = "some-bucket"

    enrolment_id = test_data.enrolment_id

    get_callbacks_list.return_value = DataProvider.callbacks_list1

    enrolment_status = repo.get_enrolment_status(enrolment_id)

    assert enrolment_status == test_data.enrolment_status1


@mock.patch("json.loads")
@mock.patch("boto3.client")
def test_get_enrolment_status_empty(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.CALLBACK_BUCKET = "some-bucket"

    enrolment_id = test_data.enrolment_id
    callback = test_data.sample_callback.dict()

    boto_client.return_value.list_objects = list_objects_sample_content_empty
    json_loads.return_value = callback

    enrolment_status = repo.get_enrolment_status(enrolment_id)

    assert enrolment_status == {
        "status": {
            "total_callbacks": "0",
            "most_recent_callback": "",
        }
    }


@mock.patch("json.loads")
@mock.patch("boto3.client")
def test_get_callback(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.CALLBACK_BUCKET = "some-bucket"

    enrolment_id = test_data.enrolment_id
    callback_id = test_data.callback_id
    sample_callback = test_data.sample_callback

    boto_client.return_value.list_objects = list_objects_sample_content
    json_loads.return_value = test_data.sample_callback.dict()
    enrolment = repo.get_callback(enrolment_id, callback_id)

    assert enrolment == sample_callback
    boto_client.return_value.get_object.assert_called_once_with(
        Key=f"callbacks/{enrolment_id}.json",
        Bucket=settings.ENROLMENT_BUCKET,
    )


@mock.patch("json.loads")
@mock.patch("boto3.client")
def test_get_callback_not_in_list(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.CALLBACK_BUCKET = "some-bucket"

    enrolment_id = test_data.enrolment_id
    callback_id = test_data.callback_id

    boto_client.return_value.list_objects = list_objects_sample_content
    json_loads.return_value = test_data.sample_callback1.dict()

    exception = ""
    try:
        enrolment = repo.get_callback(enrolment_id, callback_id)
        print(enrolment)
    except Exception as e:
        exception = e.args[0]

    assert exception == f"Callback with callback_id={callback_id} does not exist!"


@mock.patch("boto3.client")
def test_get_callback_not_exists(boto_client):
    repo = S3EnrolmentRepo()
    settings.CALLBACK_BUCKET = "some-bucket"

    enrolment_id = test_data.enrolment_id
    callback_id = test_data.callback_id

    boto_client.list_objects.side_effect = Exception()

    exception = ""
    try:
        enrolment = repo.get_callback(enrolment_id, callback_id)
        print(enrolment)
    except Exception as e:
        exception = e.args[0]

    assert exception == f"Callback with callback_id={callback_id} does not exist!"


def test_is_reference_unique():
    repo = S3EnrolmentRepo()
    internal_reference = test_data.internal_reference

    response = repo.is_reference_unique(internal_reference)

    assert response is True


@mock.patch("boto3.client")
def test_is_reference_unique_false(boto_client):
    repo = S3EnrolmentRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"
    internal_reference = test_data.internal_reference

    boto_client.return_value.get_object = object_sample_content

    response = repo.is_reference_unique(internal_reference)

    assert response is False


@mock.patch("boto3.client")
def test_enrolment_exists(boto_client):
    repo = S3EnrolmentRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"

    enrolment_id = test_data.enrolment_id
    response = repo.enrolment_exists(enrolment_id, bucket=settings.ENROLMENT_BUCKET)

    assert response is True
    boto_client.return_value.get_object.assert_called_once_with(
        Key=f"enrolments/{enrolment_id}.json",
        Bucket=settings.ENROLMENT_BUCKET,
    )


@mock.patch("boto3.client")
def test_enrolment_exists_false(boto_client):
    repo = S3EnrolmentRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"
    enrolment_id = test_data.enrolment_id

    boto_client.return_value.get_object = Exception()

    response = repo.enrolment_exists(enrolment_id, bucket=settings.ENROLMENT_BUCKET)

    assert response is False


def mock_datetime_now(target, datetime_module):
    """Override ``datetime.datetime.now()`` with a custom target value.
    This creates a new datetime.datetime class, and alters its now()/utcnow()
    methods.
    Returns:
        A mock.mock.patch context, can be used as a decorator or in a with.
    """
    real_datetime_class = datetime.datetime

    class DatetimeSubclassMeta(type):
        """We need to customize the __instancecheck__ method for isinstance().
        This must be performed at a metaclass level.
        """

        @classmethod
        def __instancecheck__(mcs, obj):
            return isinstance(obj, real_datetime_class)

    class BaseMockedDatetime(real_datetime_class):
        @classmethod
        def now(cls, tz=None):
            return target.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return target

    # Python2 & Python3-compatible metaclass
    MockedDatetime = DatetimeSubclassMeta("datetime", (BaseMockedDatetime,), {})

    return mock.patch.object(datetime_module, "datetime", MockedDatetime)


def object_sample_content(Key, Bucket):
    return {"Body": test_data.sample_enrolment}


def list_objects_sample_content(Bucket, Prefix):
    return {
        "Contents": [
            {
                "enrolment_id": test_data.enrolment_id,
                "bucket": Bucket,
                "prefix": Prefix,
                "Key": "callbacks/" + test_data.enrolment_id + ".json",
            }
        ]
    }


def list_objects_sample_content_empty(Bucket, Prefix):
    return {}
