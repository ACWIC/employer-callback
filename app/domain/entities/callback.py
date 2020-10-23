import base64
import json
import string
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator

from app.requests.callback_requests import CallbackRequest


class Attachment(BaseModel):
    """
    Represents a callback event attachment,
    an attachment has a name and a base64 encoded content.
    the name is a pathlike string with no whitespaces.
    """

    name: str
    content: bytes

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create an Attachment model instance with content as
        base64 encoded value.
        """
        content = data.get("content")
        content_encoded = base64.b64encode(content)
        data.update({"content": content_encoded})

        return cls(**data)

    @validator("name")
    def path_like_name(cls, value):
        """
        validate that an attachment's name is URL like,
        ( has a path like form but with no whitespaces )
        """
        # for now only check that the name doesn't contain any whitespaces
        for c in string.whitespace:
            if c in value:
                raise ValueError("Provided name contains whitespaces")
        return value

    @property
    def content_decoded(self):
        """
        return a valid decoded value of the Attachment encoded content.
        """
        return base64.b64decode(self.content)


class CallbackEvent(BaseModel):
    #  event metadata
    callback_id: UUID = Field(default_factory=uuid4)
    received: datetime = Field(default_factory=datetime.now)  # maybe use UTC
    sender_sequence: int
    message_type_version: str
    shared_secret: str

    #  event content
    enrolment_id: str
    structured_data: bytes
    attachments: List[Attachment]

    @classmethod
    def from_request(cls, request: CallbackRequest):
        """
        Create a CallbackEvent instance with proper typing from
        provided basic data.

        this is implemented as a convenience to avoid duplicating
        fields
        serializeion code needed for both `structured_data` & `attachments`
        """
        structured_data = base64.b64encode(
            json.dumps(request.structured_data).encode("utf-8")
        )
        attachments = [Attachment.from_dict(attach) for attach in request.attachments]
        data = request.dict()
        data.update({"structured_data": structured_data, "attachments": attachments})

        return cls(**data)

    @property
    def uid(self):
        """
        return callback_id UUID instance as a string.
        """
        return str(self.callback_id)

    @property
    def structured_data_decoded(self):
        """
        return a valid decoded JSON value of the event's structured_data
        """
        decoded_data = base64.b64decode(self.structured_data)
        return json.loads(decoded_data)

    @validator("message_type_version")
    def validate_message_type(cls, value):
        """
        Validate message type version based on available versions.

        for now this only validates that it's not an empty string
        """
        if not value:
            raise ValueError("message type version must not be an empty string")
        return value

    def serialize(self):
        """
        Return a utf-8 encoded json representation of a CallbackEvent instance.
        """
        return bytes(self.json(), "utf-8")
