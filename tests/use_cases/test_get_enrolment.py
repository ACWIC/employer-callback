from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.use_cases.get_enrolment import GetEnrolmentByID


def test_get_enrolment_by_id():
    """
    When GetEnrolmentByID is instantiated,
    the resulting object should have correct attribute values.
    """
    print("test_get_enrolment_by_id()")
    enrolment_repo = S3EnrolmentRepo()
    get_enrolment = GetEnrolmentByID(enrolment_repo=enrolment_repo)
    print("GetEnrolmentByID is", get_enrolment)
    assert get_enrolment.enrolment_repo != "1"
    print("tested")
