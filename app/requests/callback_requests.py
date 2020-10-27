from typing import List, Optional

from app.requests import ValidRequest


class AttachmentRequest(ValidRequest):
    name: str
    content: str


class CallbackRequest(ValidRequest):
    sender_sequence: int
    message_type_version: str
    shared_secret: str
    enrolment_id: str
    structured_data: dict
    attachments: Optional[List[AttachmentRequest]]
