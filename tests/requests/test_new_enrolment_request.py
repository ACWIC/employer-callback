from app.requests.enrolment_requests import NewEnrolmentRequest


def test_new_enrolment_request():
    """
    When a NewEnrollmentRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    request = NewEnrolmentRequest(
        student_id='some-student-id',
        course_id='course'
    )

    assert request.student_id == 'some-student-id'
    assert request.course_id == 'course'
