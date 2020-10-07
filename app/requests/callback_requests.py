from app.requests import ValidRequest
from uuid import UUID


class CallbackRequest(ValidRequest):
    enrolment_id: UUID
    key: UUID
    tp_sequence: int
    payload: dict
