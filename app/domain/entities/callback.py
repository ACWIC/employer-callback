import base64
import json
import string
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from app.requests.callback_requests import AttachmentRequest, CallbackRequest
from app.utils import Random
from app.utils.error_handling import handle_base64_errors


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
        if isinstance(content, str):
            content = bytes(content, "utf-8")
        with handle_base64_errors():
            content_encoded = base64.urlsafe_b64encode(content)
        data.update({"content": content_encoded})

        return cls(**data)

    @classmethod
    def from_request(cls, data: AttachmentRequest):
        """
        Create an Attachment model instance with content as
        base64 encoded value.
        """
        data = data.dict()
        return cls.from_dict(data)

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
        with handle_base64_errors():
            return base64.urlsafe_b64decode(self.content)


class Callback(BaseModel):
    #  event receipt
    callback_id: str = Field(default_factory=Random().get_uuid)
    received: datetime = Field(default_factory=datetime.now)  # maybe use UTC

    #  event metadata
    enrolment_id: str
    sender_sequence: int
    message_type_version: str
    shared_secret: str

    #  event content
    structured_data: bytes
    attachments: Optional[List[Attachment]]

    @classmethod
    def from_request(cls, request: CallbackRequest):
        """
        Create a CallbackEvent instance with proper typing from
        provided basic data.

        this is implemented as a convenience to avoid duplicating
        fields
        serialization code needed for both `structured_data` & `attachments`
        """
        with handle_base64_errors():
            structured_data = base64.urlsafe_b64encode(
                json.dumps(request.structured_data).encode("utf-8")
            )
        data = request.dict()
        data.update({"structured_data": structured_data})
        if request.attachments:
            attachments = [
                Attachment.from_request(attach) for attach in request.attachments
            ]
            data.update({"attachments": attachments})

        return cls(**data)

    @property
    def structured_data_decoded(self):
        """
        return a valid decoded JSON value of the event's structured_data
        """
        with handle_base64_errors():
            decoded_data = base64.urlsafe_b64decode(self.structured_data)
        return json.loads(decoded_data)

    @validator("message_type_version")
    def validate_message_type(cls, value):
        """
        Validate message type version based on available versions.

        for now this only validates that it's not an empty string
        """
        if not value:
            raise ValueError("Message type version must not be an empty string!")
        return value

    def serialize(self):
        """
        Return a utf-8 encoded json representation of a CallbackEvent instance.
        """
        return bytes(self.json(), "utf-8")

    def __eq__(self, obj):
        exclude = {"callback_id", "received"}
        d1 = self.dict(exclude=exclude)
        d2 = obj.dict(exclude=exclude)
        return d1 == d2
