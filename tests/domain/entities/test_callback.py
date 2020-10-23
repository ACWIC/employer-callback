import base64
import json
from datetime import datetime
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

import app.domain.entities.callback as cb
from tests.domain.entities import factories


def test_callback_event_valid():
    """
    Ensure the callback data matches constructor values
    and the status is appropriately set.
    """
    event = factories.callback_event()

    assert isinstance(event.callback_id, UUID)
    assert isinstance(event.received, datetime)
    assert isinstance(event.enrolment_id, str)
    assert isinstance(event.sender_sequence, int)
    assert isinstance(event.message_type_version, str)
    assert isinstance(event.shared_secret, str)
    assert isinstance(event.structured_data, bytes)
    assert isinstance(event.attachments, list)
    assert isinstance(event.attachments[0], cb.Attachment)


def test_callback_event_from_request_valid():
    """
    Ensure callback event created with from_request has proper encoded
    fields.
    """
    data = {"key": "value"}
    attachment = {"name": "dummy.txt", "content": b"empty"}
    encoded_data = base64.b64encode(json.dumps(data).encode("utf-8"))
    encoded_content = base64.b64encode(b"empty")
    event = factories.callback_event_from_request(
        structured_data=data, attachments=[attachment]
    )

    assert event.structured_data == encoded_data
    assert event.structured_data_decoded == data
    assert event.attachments[0].content == encoded_content


def test_callback_without_defaults_valid():
    """
    Ensure creating a CallbackEvent instance with a provided
    callback_id and received values doesn't use the default factory.
    """
    callback_id = uuid4()
    received = datetime.now()
    event = factories.callback_event(callback_id=callback_id, received=received)

    assert event.callback_id == callback_id
    assert event.received == received


def test_attachment_from_dict_valid():
    """
    Ensure Attachment data validation and from_dict
    creates a valid attachment with encoded content.
    """
    content = b"this is an dummy file content"
    content_encoded = base64.b64encode(content)
    attachment = factories.attachment_from_dict(content=content)

    assert attachment.name == "dummy.txt"
    assert attachment.content == content_encoded
    assert attachment.content_decoded == content


def test_attachment_name_with_spaces_invalid():
    """
    Ensure that an attachment name value with whitespaces
    will raise a validation error.
    """
    name = "dummy with spaces.txt"

    with pytest.raises(ValidationError) as excinfo:
        _ = factories.attachment_from_dict(name=name)

    assert "Provided name contains whitespaces" in str(excinfo.value)
