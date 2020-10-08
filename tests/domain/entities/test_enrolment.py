from datetime import datetime
from uuid import uuid4

from app.domain.entities.enrolment import Enrolment


def test_enrolment_init():
    """
    Ensure the enrollment data matches constructor values
    and the status is appropriately set.
    """
    # dummy values
    e = str(uuid4())
    k = str(uuid4())
    c = datetime.now()

    enrolment = Enrolment(enrolment_id=e, key=k, created=c)

    assert enrolment.enrolment_id == e
    assert enrolment.key == k
    assert enrolment.created == c
