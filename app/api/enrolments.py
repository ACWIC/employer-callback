from fastapi import APIRouter, HTTPException
from app.requests.callback_requests import CallbackRequest
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.use_cases.create_new_callback import CreateNewCallback


router = APIRouter()


@router.post("/enrolments")
def create_enrolment(inputs: CallbackRequest):
    callback_repo = S3EnrolmentRepo()
    use_case = CreateNewEnrolment(callback_repo=callback_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(response.message, status_code=response.status_code)

    return response
