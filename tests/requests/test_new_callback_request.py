from tests.test_data.callback_provider import CallbackDataProvider


def test_new_callback_request():
    """
    When a NewCallbackRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    request = CallbackDataProvider().sample_callback_request

    assert isinstance(request.sender_sequence, int)
    assert isinstance(request.message_type_version, str)
    assert isinstance(request.shared_secret, str)
    assert isinstance(request.enrolment_id, str)
    assert isinstance(request.structured_data, dict)


def test_new_callback_request_with_attachment():
    """
    When a NewCallbackRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    request = CallbackDataProvider().sample_callback_request_with_attachment

    assert isinstance(request.sender_sequence, int)
    assert isinstance(request.message_type_version, str)
    assert isinstance(request.shared_secret, str)
    assert isinstance(request.enrolment_id, str)
    assert isinstance(request.structured_data, dict)
    assert isinstance(request.attachments, list)
