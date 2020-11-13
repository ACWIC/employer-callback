import base64
import json
from datetime import datetime

import pytest
from pydantic import ValidationError

import app.domain.entities.callback as cb
from app.requests.callback_requests import AttachmentRequest
from app.utils import Random
from tests.test_data.callback_data_provider import CallbackDataProvider

test_data = CallbackDataProvider()


def test_callback_valid():
    """
    Ensure the callback data matches constructor values
    and the status is appropriately set.
    """
    event = test_data.sample_callback

    assert isinstance(event.callback_id, str)
    assert isinstance(event.received, datetime)
    assert isinstance(event.enrolment_id, str)
    assert isinstance(event.sender_sequence, int)
    assert isinstance(event.message_type_version, str)
    assert isinstance(event.shared_secret, str)
    assert isinstance(event.structured_data, bytes)


def test_callback_valid_with_attachment():
    """
    Ensure the callback data matches constructor values
    and the status is appropriately set.
    """
    event = test_data.sample_callback_with_attachment

    assert isinstance(event.callback_id, str)
    assert isinstance(event.received, datetime)
    assert isinstance(event.enrolment_id, str)
    assert isinstance(event.sender_sequence, int)
    assert isinstance(event.message_type_version, str)
    assert isinstance(event.shared_secret, str)
    assert isinstance(event.structured_data, bytes)
    assert isinstance(event.attachments, list)
    assert isinstance(event.attachments[0], cb.Attachment)


def test_callback_from_request_valid():
    """
    Ensure callback event created with from_request has proper encoded
    fields.
    """
    data = {"key": "value"}
    encoded_data = base64.urlsafe_b64encode(json.dumps(data).encode("utf-8"))
    request = test_data.sample_callback_request
    request.structured_data = data
    request.attachments = [test_data.attachment]
    event = cb.Callback.from_request(request)

    assert event.structured_data == encoded_data
    assert event.structured_data_decoded == data
    assert event.attachments[0].content_decoded == test_data.attachment.content


def test_callback_without_defaults_valid():
    """
    Ensure creating a CallbackEvent instance with a provided
    callback_id and received values doesn't use the default factory.
    """
    callback_id = Random().get_uuid()
    received = datetime.now()
    callback_dict = test_data.sample_callback_dict
    callback_dict.update({"callback_id": callback_id, "received": received})
    event = cb.Callback(**callback_dict)

    assert event.callback_id == callback_id
    assert event.received == received


def test_attachment_from_dict_valid():
    """
    Ensure Attachment data validation and from_dict
    creates a valid attachment with encoded content.
    """
    content = b"this is an dummy file content"
    content_encoded = base64.b64encode(content)
    attachment = cb.Attachment.from_dict({"content": content, "name": "dummy.txt"})

    assert attachment.name == "dummy.txt"
    assert attachment.content == content_encoded
    assert attachment.content_decoded == content


def test_attachment_name_with_spaces_invalid():
    """
    Ensure that an attachment name value with whitespaces
    will raise a validation error.
    """
    name = "dummy with spaces.txt"
    content = b"this is an dummy file content"
    content_encoded = base64.b64encode(content)
    with pytest.raises(ValidationError) as excinfo:
        cb.Attachment.from_dict({"content": content_encoded, "name": name})

    assert "Provided name contains whitespaces" in str(excinfo.value)


def test_attachment_content_str_valid():
    """
    Ensure Attachment data validation and from_dict
    creates a valid attachment with encoded content
    even content type is string.
    """
    content = "this is an dummy file content"
    byte_content = bytes(content, "utf-8")
    content_encoded = base64.b64encode(byte_content)
    attachment = cb.Attachment.from_dict({"content": content, "name": "dummy.txt"})

    assert attachment.name == "dummy.txt"
    assert attachment.content == content_encoded
    assert attachment.content_decoded == byte_content


def test_attachment_from_request_valid():
    """
    Ensure Attachment data validation and from_request
    creates a valid attachment with encoded content.
    """
    content = "this is an dummy file content"
    byte_content = bytes(content, "utf-8")
    content_encoded = base64.b64encode(byte_content)
    request = AttachmentRequest(content=content, name="dummy.txt")
    attachment = cb.Attachment.from_request(request)

    assert attachment.name == "dummy.txt"
    assert attachment.content == content_encoded
    assert attachment.content_decoded == byte_content


def test_message_type_version_invalid():
    callback_dict = test_data.sample_callback_dict
    callback_dict.update({"message_type_version": ""})
    with pytest.raises(ValueError) as exception:
        cb.Callback(**callback_dict)
    assert "Message type version must not be an empty string!" in str(exception.value)


def test_callback_compare_true():
    callback_1 = test_data.sample_callback
    callback_2 = test_data.sample_callback
    assert callback_1 == callback_2


def test_callback_compare_false():
    callback_1 = test_data.sample_callback
    callback_2 = test_data.sample_callback_2
    assert callback_1 != callback_2
