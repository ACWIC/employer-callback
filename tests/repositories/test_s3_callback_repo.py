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

from botocore.stub import Stubber

from app.config import settings
from app.repositories.s3_callback_repo import S3CallbackRepo
from tests.test_data.boto_client_responses import (
    get_object_response,
    list_objects_response,
)
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
        Bucket=settings.CALLBACK_BUCKET,
    )


@patch("json.loads")
def test_save_callback_already_exists(json_loads):
    repo = S3CallbackRepo()
    stubber = Stubber(repo.s3)
    callback = CallbackDataProvider().sample_callback
    callback_id = CallbackDataProvider().callback_id
    callback_dict = CallbackDataProvider().sample_callback_dict
    stubber.add_response(
        "list_objects",
        list_objects_response([callback_id]),
        {"Bucket": "put-callbacks-here"},
    )
    stubber.add_response(
        "get_object",
        get_object_response(callback),
        {"Bucket": "put-callbacks-here", "Key": CallbackDataProvider().callback_id},
    )
    json_loads.return_value = callback.to_dict()
    with stubber:
        is_created, callback_obj = repo.save_callback(callback_dict)

    assert is_created is False
    assert callback_obj == callback


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
    callback_id = CallbackDataProvider().callback_id
    stubber = Stubber(repo.s3)
    json_loads.return_value = callback.to_dict()
    stubber.add_response(
        "list_objects",
        list_objects_response([callback_id]),
        {"Bucket": "put-callbacks-here"},
    )
    stubber.add_response(
        "get_object",
        get_object_response(callback),
        {"Bucket": "put-callbacks-here", "Key": CallbackDataProvider().callback_id},
    )
    with stubber:
        is_exists, callback_obj = repo.is_callback_already_exists(callback)

    assert is_exists is True
    assert callback_obj == callback


@patch("json.loads")
def test_is_callback_already_exists_false(json_loads):
    repo = S3CallbackRepo()
    callback = CallbackDataProvider().sample_callback
    callback_id = CallbackDataProvider().callback_id
    callback_2 = CallbackDataProvider().sample_callback_2
    stubber = Stubber(repo.s3)
    json_loads.return_value = callback_2.to_dict()
    stubber.add_response(
        "list_objects",
        list_objects_response([callback_id]),
        {"Bucket": "put-callbacks-here"},
    )
    stubber.add_response(
        "get_object",
        get_object_response(callback_2),
        {"Bucket": "put-callbacks-here", "Key": callback_id},
    )
    with stubber:
        is_exists, callback_obj = repo.is_callback_already_exists(callback)

    assert is_exists is False
    assert callback_obj is None
