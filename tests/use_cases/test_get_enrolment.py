from unittest import mock

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.responses import FailureType, SuccessType
from app.use_cases.get_enrolment import GetEnrolmentByID
from tests.test_data.enrolment_data_provider import DataProvider


def test_get_enrolment_success():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment_id = DataProvider().enrolment_id
    repo.enrolment_exists.return_value = True
    repo.get_enrolment.return_value = DataProvider().sample_enrolment

    use_case = GetEnrolmentByID(enrolment_repo=repo)
    response = use_case.execute(enrolment_id)

    assert response.type == SuccessType.SUCCESS


def test_get_enrolment_not_exists():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment_id = DataProvider().enrolment_id
    repo.enrolment_exists.return_value = False
    repo.get_enrolment.return_value = DataProvider().sample_enrolment

    use_case = GetEnrolmentByID(enrolment_repo=repo)
    response = use_case.execute(enrolment_id)

    assert response.type == FailureType.VALIDATION_ERROR


def test_get_enrolment_failure():
    repo = mock.Mock(spec=S3EnrolmentRepo)
    enrolment_id = DataProvider().enrolment_id
    repo.enrolment_exists.return_value = True

    repo.get_enrolment.side_effect = Exception()

    use_case = GetEnrolmentByID(enrolment_repo=repo)
    response = use_case.execute(enrolment_id)

    assert response.type == FailureType.RESOURCE_ERROR
