"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
import json
from datetime import datetime
from io import BytesIO
from os import environ
from unittest.mock import patch

from botocore.stub import Stubber
from fastapi.encoders import jsonable_encoder

from app.config import settings
from app.repositories.s3_callback_repo import S3CallbackRepo
from tests.test_data.callback_provider import CallbackDataProvider


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
        Key=f"callbacks/{callback.enrolment_id}/{callback.callback_id}.json",
        # NOQA
        Bucket=settings.CALLBACK_BUCKET,
    )


@patch("boto3.client")
def test_is_callback_already_exists_empty_callbacks(boto_client):
    repo = S3CallbackRepo()
    callback = CallbackDataProvider().sample_callback
    boto_client.return_value.list_objects = list_objects_empty_content
    is_exists, callback_obj = repo.is_callback_already_exists(callback)

    assert is_exists is False
    assert callback_obj is None


def list_objects_empty_content(Bucket):
    return {}


@patch("json.loads")
def test_is_callback_already_exists_true(json_loads):
    repo = S3CallbackRepo()
    callback = CallbackDataProvider().sample_callback
    stubber = Stubber(repo.s3)
    json_loads.return_value = callback.to_dict()
    stubber.add_response(
        "list_objects", list_objects(), {"Bucket": "put-callbacks-here"}
    )
    stubber.add_response(
        "get_object", get_object(), {"Bucket": "put-callbacks-here", "Key": "string"}
    )
    with stubber:
        is_exists, callback_obj = repo.is_callback_already_exists(callback)

    assert is_exists is True
    assert callback_obj == callback


def list_objects():
    return {
        "IsTruncated": True | False,
        "Marker": "string",
        "NextMarker": "string",
        "Contents": [
            {
                "Key": "string",
                "LastModified": datetime(2015, 1, 1),
                "ETag": "string",
                "Size": 123,
                "StorageClass": "STANDARD",
                "Owner": {"DisplayName": "string", "ID": "string"},
            },
        ],
        "Name": "string",
        "Prefix": "string",
        "Delimiter": "string",
        "MaxKeys": 123,
        "CommonPrefixes": [
            {"Prefix": "string"},
        ],
        "EncodingType": "url",
    }


def get_object():
    callback = CallbackDataProvider().sample_callback
    callback = json.dumps(jsonable_encoder(callback.to_dict()), indent=2).encode(
        "utf-8"
    )
    output = BytesIO()
    output.write(callback)
    return {
        "Body": output,
        "DeleteMarker": True,
        "AcceptRanges": "string",
        "Expiration": "string",
        "Restore": "string",
        "LastModified": datetime(2015, 1, 1),
        "ContentLength": 123,
        "ETag": "string",
        "MissingMeta": 123,
        "VersionId": "string",
        "CacheControl": "string",
        "ContentDisposition": "string",
        "ContentEncoding": "string",
        "ContentLanguage": "string",
        "ContentRange": "string",
        "ContentType": "string",
        "Expires": datetime(2015, 1, 1),
        "WebsiteRedirectLocation": "string",
        "ServerSideEncryption": "AES256",
        "Metadata": {"string": "string"},
        "SSECustomerAlgorithm": "string",
        "SSECustomerKeyMD5": "string",
        "SSEKMSKeyId": "string",
        "StorageClass": "STANDARD",
        "RequestCharged": "requester",
        "ReplicationStatus": "COMPLETE",
        "PartsCount": 123,
        "TagCount": 123,
        "ObjectLockMode": "GOVERNANCE",
        "ObjectLockRetainUntilDate": datetime(2015, 1, 1),
        "ObjectLockLegalHoldStatus": "ON",
    }
