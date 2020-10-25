from unittest.mock import patch

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.responses import SuccessType
from app.use_cases.get_enrolment import GetEnrolmentByID
from tests.test_data.callback_provider import CallbackDataProvider


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

    get_enrolment.return_value = CallbackDataProvider().sample_enrolment
    response = use_case.execute(CallbackDataProvider().enrolment_id)
    assert response.type == SuccessType.SUCCESS
    assert response.value["enrolment_id"] == CallbackDataProvider().enrolment_id
