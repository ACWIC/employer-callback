from datetime import datetime
from uuid import uuid4

import app.domain.entities.callback as cb
import app.domain.entities.enrolment as en
import app.requests.callback_requests as cbr


def enrolment(**overrides):
    data = {
        "enrolment_id": overrides.get("enrolment_id") or str(uuid4()),
        "shared_secret": overrides.get("shared_secret") or "shared-super-secret",
        "internal_reference": overrides.get("internal_reference") or "dummy-ref",
        "created": overrides.get("created") or datetime.now(),
    }
    return en.Enrolment(**data)


def attachment(**overrides):
    name = overrides.get("name") or "dummy.txt"
    content = overrides.get("content") or b"ZW1wdHkgZmlsZSBjb250ZW50"

    return cb.Attachment(**{"name": name, "content": content})


def attachment_from_dict(**overrides):
    name = overrides.get("name") or "dummy.txt"
    content = overrides.get("content") or b"empty none decoded content"

    return cb.Attachment.from_dict({"name": name, "content": content})


def callback_event(**overrides):
    data = {
        "enrolment_id": overrides.get("enrolment_id") or "this-is-my-enrolment-id",
        "sender_sequence": overrides.get("sender_sequence") or 1,
        "message_type_version": overrides.get("message_type_version") or "v1",
        "shared_secret": overrides.get("shared_secret")
        or "this-is-my-super-secret-key",
        "structured_data": overrides.get("structured_data")
        or b"eyJrZXkiOiAidmFsdWUiLCAiYW5vdGhlcl9rZXkiOiAiYW5vdGhlciB2YWx1ZSJ9",
        "attachments": overrides.get("attachments")
        or [{"name": "dummy.txt", "content": b"ZW1wdHk="}],
    }

    callback_id = overrides.get("callback_id")
    if callback_id:
        data.update({"callback_id": callback_id})

    received = overrides.get("received")
    if received:
        data.update({"received": received})

    return cb.Callback(**data)


def callback_event_from_request(request=None, **overrides):
    if not request:
        data = {
            "enrolment_id": overrides.get("enrolment_id") or "this-is-my-enrolment-id",
            "sender_sequence": overrides.get("sender_sequence") or 1,
            "message_type_version": overrides.get("message_type_version") or "v1",
            "shared_secret": overrides.get("shared_secret")
            or "this-is-my-super-secret-key",
            "structured_data": overrides.get("structured_data")
            or {"key": "value", "another_key": "another value"},
            "attachments": overrides.get("attachments")
            or [{"name": "dummy.txt", "content": b"empty"}],
        }
        request = cbr.CallbackRequest(**data)

    return cb.Callback.from_request(request)
