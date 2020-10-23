from tests.requests import factories


def test_new_callback_request():
    """
    When a NewCallbackRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    request = factories.callback_request()

    assert isinstance(request.sender_sequence, int)
    assert isinstance(request.message_type_version, str)
    assert isinstance(request.shared_secret, str)
    assert isinstance(request.enrolment_id, str)
    assert isinstance(request.structured_data, dict)
    assert isinstance(request.attachments, list)
