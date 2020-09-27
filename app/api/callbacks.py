from fastapi import APIRouter
from app.requests.enrolment_requests import NewEnrolmentRequest
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.use_cases.create_new_enrolment import CreateNewEnrolment


router = APIRouter()


@router.get('/enrolments/{enrolment_id}')
def enrolments(enrolment_id: str):
    ''' Getting an enrollment by ID will return the current
        state of the enrollment, derived from the enrollment’s journal.
    '''
    return {"your_enrolment_id": enrolment_id}


@router.post("/enrolments")
def create_enrolment(inputs: NewEnrolmentRequest):
    ''' Posting an enrollment authorisation is a synchronous proccess that
        immediately succeeds (or fails) to create an enrollment authorisation,
        and assign it a unique enrollment authorisation id.

        The initial state of the enrollment authorisation is “lodged”.
    '''
    enrolment_repo = S3EnrolmentRepo()
    use_case = CreateNewEnrolment(enrolment_repo=enrolment_repo)
    response = use_case.execute(inputs)

    return response
