from app.requests import ValidRequest


class NewEnrolmentRequest(ValidRequest):
    course_id: str
    student_id: str
