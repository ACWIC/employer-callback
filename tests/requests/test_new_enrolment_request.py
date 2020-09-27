from app.requests.callback_requests import CallbackRequest


def test_new_callback_request():
    """
    When a NewCallbackRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    # dummy data
    key = 'employer_made_this'
    e_id = 'employer_made_this'
    tp_seq = 76543567
    pl = {"days": "hapy"}

    request = CallbackRequest(
        enrolment_id=e_id,
        key=key,
        tp_sequence=tp_seq,
        payload=pl
    )

    assert request.enrolment_id == e_id
    assert request.key == key
    assert request.tp_sequence == tp_seq
    assert request.payload == pl
