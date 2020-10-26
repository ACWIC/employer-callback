import datetime

import app.domain.entities.callback as cb
from tests.test_data.callback_provider import CallbackDataProvider


def test_callback_init():
    """
    Ensure the callback data matches constructor values
    and the status is appropriately set.
    """
    cb_id = "this-is-callback-id"
    e_id = "this-is-my-enrolment-id"
    k = "this-is-my-key"
    tp_ref = 123456
    rx = datetime.datetime.now()
    pl = {"ham": "eggs"}
    callback = cb.Callback(
        callback_id=cb_id,
        enrolment_id=e_id,
        shared_secret=k,
        tp_sequence=tp_ref,
        received=rx,
        payload=pl,
    )

    assert callback.callback_id == cb_id
    assert callback.enrolment_id == e_id
    assert callback.shared_secret == k
    assert callback.tp_sequence == tp_ref
    assert callback.received == rx
    assert callback.payload == pl


def test_callback_compare_true():
    callback_1 = CallbackDataProvider().sample_callback
    callback_2 = CallbackDataProvider().sample_callback
    assert callback_1 == callback_2


def test_callback_compare_false():
    callback_1 = CallbackDataProvider().sample_callback
    callback_2 = CallbackDataProvider().sample_callback_2
    assert callback_1 != callback_2
