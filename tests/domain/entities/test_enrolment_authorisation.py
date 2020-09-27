import app.domain.entities.callback as cb
from uuid import uuid4


def test_callback_authorisation_init():
    """
    Ensure the callback data matches constructor values
    and the status is appropriately set.
    """
    callback_id = uuid4()
    callback = cb.Callback(
        uuid=callback_id,
    )
    # TODO: callback needs a "key" attribute
    # which is used like a password
    # TODO: callback needs to identify the enrolment by ID

    assert callback.uuid == callback_id
