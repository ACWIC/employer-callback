from app.requests.enrolment_requests import NewEnrolmentRequest


def test_new_enrolment_request():
    """
    When a NewEnrollmentRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    ref = "some-reference"
    request = NewEnrolmentRequest(internal_reference=ref)

    assert request.internal_reference == ref
