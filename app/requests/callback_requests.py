from app.requests import ValidRequest


class NewCallbackRequest(ValidRequest):
    enrolment_id: str
    key: str
