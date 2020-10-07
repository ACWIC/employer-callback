from app.requests import ValidRequest


class CallbackRequest(ValidRequest):
    enrolment_id: str
    key: str
    tp_sequence: int
    payload: dict
    invalid: dict
