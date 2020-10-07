import datetime
from uuid import uuid4

import app.domain.entities.callback as cb


def test_callback_init():
    """
    Ensure the callback data matches constructor values
    and the status is appropriately set.
    """
    cb_id = uuid4()
    e_id = "this-is-my-enrolment-id"
    k = "this-is-my-key"
    tp_ref = 123456
    rx = datetime.datetime.now()
    pl = {"ham": "eggs"}
    callback = cb.Callback(
        callback_id=cb_id,
        enrolment_id=e_id,
        key=k,
        tp_sequence=tp_ref,
        received=rx,
        payload=pl,
    )

    assert callback.callback_id == cb_id
    assert callback.enrolment_id == e_id
    assert callback.key == k
    assert callback.tp_sequence == tp_ref
    assert callback.received == rx
    assert callback.payload == pl
