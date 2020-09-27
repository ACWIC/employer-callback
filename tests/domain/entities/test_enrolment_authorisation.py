import app.domain.entities.enrolment_authorisation as ea
from uuid import uuid4


def test_enrolment_authorisation_init():
    """
    Ensure the enrollment data matches constructor values
    and the status is appropriately set.
    """
    enrolment_id = uuid4()
    enrolment = ea.EnrolmentAuthorisation(
        uuid=enrolment_id,
        course_id='course-id',
        student_id='1234'
    )

    assert enrolment.uuid == enrolment_id
    assert enrolment.student_id == '1234'
    assert enrolment.course_id == 'course-id'
    # TODO: make a statehart for documentation
    # then test it - probably not lodged unti lodgement!
    assert enrolment.status == ea.EnrolmentStatus.lodged
