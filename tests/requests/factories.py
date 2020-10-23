from app.requests.callback_requests import CallbackRequest


def callback_request(**overrides):
    data = {
        "sender_sequence": overrides.get("sender_sequence") or 9876543,
        "shared_secret": overrides.get("shared_secret")
        or "the_employer_generated_this_secret",
        "message_type_version": overrides.get("message_type_version") or "v1",
        "enrolment_id": overrides.get("enrolment_id")
        or "the_employer_generated_this_identifier",
        "structured_data": overrides.get("structured_data")
        or {"key": "value", "another_key": "another value"},
        "attachments": overrides.get("attachments")
        or [{"name": "dummy.txt", "content": b"empty"}],
    }

    return CallbackRequest(**data)
