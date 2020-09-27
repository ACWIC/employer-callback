from app.requests.callback_requests import NewCallbackRequest


def test_new_callback_request():
    """
    When a NewCallbackRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    key = 'employer_made_this'
    enrolment_id = 'employer_made_this'
    request = NewCallbackRequest(
        enrolment_id=enrolment_id,
        key=key
    )

    # TODO: assert what we know about callback requests
    # grep for TODO...
