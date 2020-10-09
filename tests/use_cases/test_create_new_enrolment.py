"""
These tests evaluate (and document) the business logic.
"""
from datetime import datetime
from unittest import mock
from uuid import uuid4

from app.domain.entities.enrolment import Enrolment
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.enrolment_requests import NewEnrolmentRequest
from app.responses import FailureType, SuccessType
from app.use_cases.create_new_enrolment import CreateNewEnrolment

dummy_key = str(uuid4())
dummy_created = datetime.now()
dummy_enrolment = str(uuid4())
dummy_internal_reference = str(uuid4())


def test_create_new_enrolment_success():
    """
    When creating a new enrollment,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=S3EnrolmentRepo)
    repo.is_reference_unique.return_value = True

    enrolment = Enrolment(
        enrolment_id=dummy_enrolment,
        internal_reference=dummy_internal_reference,
        shared_secret=dummy_key,
        created=dummy_created,
    )
    repo.save_enrolment.return_value = enrolment

    request = NewEnrolmentRequest(internal_reference=dummy_internal_reference)
    use_case = CreateNewEnrolment(enrolment_repo=repo)
    response = use_case.execute(request)

    assert response.type == SuccessType.SUCCESS


def test_create_new_enrolment_failure():
    """
    When creating a new enrollment,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=S3EnrolmentRepo)

    repo.save_enrolment.side_effect = Exception()
    request = NewEnrolmentRequest(internal_reference=dummy_enrolment)
    use_case = CreateNewEnrolment(enrolment_repo=repo)
    response = use_case.execute(request)

    assert response.type == FailureType.RESOURCE_ERROR
