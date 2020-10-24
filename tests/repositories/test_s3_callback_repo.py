"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from unittest.mock import patch

from botocore.stub import Stubber

from app.config import settings
from app.repositories.s3_callback_repo import S3CallbackRepo
from tests.test_data.boto_client_responses import (
    get_object_response,
    list_objects_empty_response,
    list_objects_response,
)
from tests.test_data.callback_provider import CallbackDataProvider

test_data = CallbackDataProvider()


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
    repo = S3CallbackRepo()

    params = test_data.sample_callback_dict
    callback = repo.save_callback(params)

    assert callback.callback_id == test_data.callback_id

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(callback.json(), "utf-8"),
        Key=f"callbacks/{callback.enrolment_id}/{callback.callback_id}.json",
        Bucket=settings.CALLBACK_BUCKET,
    )


@patch("json.loads")
def test_save_callback_already_exists(json_loads):
    repo = S3CallbackRepo()
    stubber = Stubber(repo.s3)
    callback = test_data.sample_callback
    callback_id = test_data.callback_id
    callback_dict = test_data.sample_callback_dict
    stubber.add_response(
        "list_objects",
        list_objects_response([callback_id]),
        {"Bucket": "put-callbacks-here"},
    )
    stubber.add_response(
        "get_object",
        get_object_response(callback),
        {"Bucket": "put-callbacks-here", "Key": test_data.callback_id},
    )
    json_loads.return_value = callback.to_dict()
    with stubber:
        callback_obj = repo.save_callback(callback_dict)

    assert callback_obj == callback


def test_callback_exists_empty_callbacks():
    repo = S3CallbackRepo()
    callback = test_data.sample_callback
    stubber = Stubber(repo.s3)
    stubber.add_response(
        "list_objects",
        list_objects_empty_response(),
        {"Bucket": "put-callbacks-here"},
    )
    with stubber:
        assert repo.callback_exists(callback.to_dict()) is False


@patch("json.loads")
def test_callback_exists_true(json_loads):
    repo = S3CallbackRepo()
    callback = test_data.sample_callback
    callback_id = test_data.callback_id
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
        {"Bucket": "put-callbacks-here", "Key": test_data.callback_id},
    )
    with stubber:
        assert repo.callback_exists(callback.to_dict()) is True


@patch("json.loads")
def test_callback_exists_true_with_cache(json_loads):
    repo = S3CallbackRepo()
    callback = test_data.sample_callback
    # add callback to cache
    repo.callbacks.append(callback)
    callback_id = test_data.callback_id
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
        {"Bucket": "put-callbacks-here", "Key": test_data.callback_id},
    )
    with stubber:
        assert repo.callback_exists(callback.to_dict()) is True
    # Assert that same callback is not appended to list
    assert len(repo.callbacks) == 1
    assert repo.callbacks[0] == callback


@patch("json.loads")
def test_callback_exists_false(json_loads):
    repo = S3CallbackRepo()
    callback = test_data.sample_callback
    callback_id = test_data.callback_id
    callback_2 = test_data.sample_callback_2
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
        assert repo.callback_exists(callback.to_dict()) is False


def test_get_callback_from_cache():
    """Ensure that get callback from cache returns correct callback object"""
    repo = S3CallbackRepo()
    callback = test_data.sample_callback
    callback_dict = test_data.sample_callback_dict
    repo.callbacks.append(callback)
    cb = repo.get_callback_from_cache(callback_dict)

    assert cb == callback


def test_get_callback_from_cache_none():
    """Ensure that get_callback_from_cache() returns None
    if callback_dict is not in cached callbacks"""
    repo = S3CallbackRepo()
    callback_dict = test_data.sample_callback_dict
    cb = repo.get_callback_from_cache(callback_dict)

    assert cb is None


def test_get_callback_from_cache_none_2():
    """Ensure that get_callback_from_cache() returns None
    if callback_dict is not in cached callbacks"""
    repo = S3CallbackRepo()
    # Push a callback that is not the same with callback_dict
    callback_2 = test_data.sample_callback_2
    repo.callbacks.append(callback_2)
    callback_dict = test_data.sample_callback_dict
    cb = repo.get_callback_from_cache(callback_dict)

    assert cb is None
