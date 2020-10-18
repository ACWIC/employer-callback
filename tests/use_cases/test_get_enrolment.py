from datetime import datetime
from unittest.mock import patch

from app.domain.entities.enrolment import Enrolment
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.responses import SuccessType
from app.use_cases.get_enrolment import GetEnrolmentByID


@patch("app.repositories.s3_enrolment_repo.S3EnrolmentRepo.get_enrolment")
def test_get_enrolment_by_id(get_enrolment):
    """
    When GetEnrolmentByID is instantiated,
    the resulting object should have correct attribute values.
    """
    print("test_get_enrolment_by_id()")
    enrolment_repo = S3EnrolmentRepo()
    use_case = GetEnrolmentByID(enrolment_repo=enrolment_repo)
    assert use_case.enrolment_repo == enrolment_repo

    get_enrolment.return_value = Enrolment(
        enrolment_id="1",
        created=datetime.now(),
        shared_secret="2323",
        internal_reference="wf2323",
    )
    response = use_case.execute("1")
    assert response.type == SuccessType.SUCCESS
    assert response.value["enrolment_id"] == "1"
