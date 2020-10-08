from app.requests.enrolment_requests import NewEnrolmentRequest


def test_new_enrolment_request():
    """
    When a NewEnrollmentRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    request = NewEnrolmentRequest(enrolment_id="some-enrolment-id")

    assert request.enrolment_id == "some-enrolment-id"
