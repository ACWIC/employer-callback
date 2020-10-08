from fastapi import APIRouter

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.enrolment_requests import NewEnrolmentRequest
from app.use_cases.create_new_enrolment import CreateNewEnrolment
from app.use_cases.get_callbacks_list import GetCallbacksList
from app.use_cases.get_enrolment import GetEnrolmentByID

router = APIRouter()
enrolment_repo = S3EnrolmentRepo()


@router.post("/enrolments")
def create_enrolment(inputs: NewEnrolmentRequest):
    """
    The Employer pre-registers a new Enrolment so callbacks can be received

    The assumption is that the employer generates a unique *enrolment_id*
    in some source system they control (LMS, HRMS, etc),
    and registers it with this microservice.
    This allows the microservice to generate keys,
    and prepare to receive callbacks from the training provider
    about this enrolment.
    """
    use_case = CreateNewEnrolment(enrolment_repo=enrolment_repo)
    response = use_case.execute(inputs)
    return response


@router.get("/enrolments/{enrolment_id}")
def get_enrolment_by_id(enrolment_id: str):  # TODO: typing, return enrolment summary
    """Return the current status of the given enrolment

    This relies on certain callbacks
    with payloads that describe state-changes in the enrolment.

    TODO:
    * negotiate a state-chart and set of message-types
      that relate to state changes.
    * use these message-types to calculate the current state
    """
    use_case = GetEnrolmentByID(enrolment_repo=enrolment_repo)
    response = use_case.execute(enrolment_id)
    return response


# GET /enrolments/{enrolment_id}/journal
@router.get("/enrolments/{enrolment_id}/journal")
def get_callbacks_list_for_enrolment(
    enrolment_id: str,
):  # TODO: typing, return enrolment summary
    """Return the current status of the given enrolment

    This relies on certain callbacks
    with payloads that describe state-changes in the enrolment.

    TODO:
    * negotiate a state-chart and set of message-types
      that relate to state changes.
    * use these message-types to calculate the current state
    """
    use_case = GetCallbacksList(enrolment_repo=enrolment_repo)
    callbacks_list = use_case.execute(enrolment_id)
    return callbacks_list
