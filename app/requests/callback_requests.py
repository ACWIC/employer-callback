from typing import List

from app.requests import ValidRequest


class CallbackRequest(ValidRequest):
    sender_sequence: int
    message_type_version: str
    shared_secret: str
    enrolment_id: str
    structured_data: dict
    attachments: List[dict]
