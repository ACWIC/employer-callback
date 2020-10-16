from app.requests import ValidRequest


class NewEnrolmentRequest(ValidRequest):
    internal_reference: str
