from fastapi import APIRouter, HTTPException

from app.repositories.s3_callback_repo import S3CallbackRepo
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.callback_requests import CallbackRequest
from app.responses import SuccessType
from app.use_cases import create_new_callback as uc

router = APIRouter()
callback_repo = S3CallbackRepo()
enrolment_repo = S3EnrolmentRepo()


@router.post("/callbacks", status_code=SuccessType.CREATED.value)
def create_callback(inputs: CallbackRequest):
    """Message from Training Provider to Employer.

    Contains information about the delivery of training services,
    is linked to student identity and employer context by enrolment_id.

    POSTing a callback is a synchronous process
    that immediately succeeds (or fails).

    The API validates the callback:

    * The posted *payload* must confirm with the CallbackRequest schema.
    * The posted *attachment* in the *payload* must confirm with the AttachmentRequest schema.
    * The *enrollment_id* parameter must be well known to the employer.
      This is a kind of "correlation id" used to associate messages.
    * The provided *key* must be valid for that enrolment_id.
      This is a kind of shared-secret, set by the employer
      and shared with the training provider
      at the time the enrolment was sent to them.
    * The returned object contains a *callback_id*.
      This is a recipient-assigned identifier,
      which may be useful in debugging.
    * The returned object contains a *received" date-time stamp,
      from the recipient's wall clock.
      Like callback_id, this may be useful in debugging.
    """
    use_case = uc.CreateNewCallback(
        callback_repo=callback_repo, enrolment_repo=enrolment_repo
    )
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()
