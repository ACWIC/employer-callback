from app.requests import ValidRequest


class NewEnrolmentRequest(ValidRequest):
    enrolment_id: str
