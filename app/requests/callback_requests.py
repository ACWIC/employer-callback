from app.requests import ValidRequest


class CallbackRequest(ValidRequest):
    enrolment_id: str
    shared_secret: str
    tp_sequence: int
    payload: dict
