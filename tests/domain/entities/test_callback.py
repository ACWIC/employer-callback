import app.domain.entities.callback as cb
from uuid import uuid4


def test_callback_authorisation_init():
    """
    Ensure the callback data matches constructor values
    and the status is appropriately set.
    """
    cb_id = uuid4()
    e_id = str(uuid4())
    k = str(uuid4())
    callback = cb.Callback(
        callback_id=cb_id,
        enrolment_id=e_id,
        key=k
    )
    # TODO: callback needs a "key" attribute
    # which is used like a password
    # TODO: callback needs to identify the enrolment by ID

    assert callback.callback_id == cb_id
    assert callback.enrolment_id == e_id
    assert callback.key == k
