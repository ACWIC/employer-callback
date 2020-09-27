from fastapi import APIRouter
from app.requests.callback_requests import CallbackRequest
from app.repositories.s3_callback_repo import S3CallbackRepo
from app.use_cases.create_new_callback import CreateNewCallback


router = APIRouter()


@router.post("/callbacks")
def create_callback(inputs: CallbackRequest):
    ''' Message from Training Provider to Employer.

    Contains information about the delivery of training services,
    is linked to student identity and employer context by enrolment_id.

    POSTing a callback is a synchronous proccess
    that immediately succeeds (or fails).

    The API validates the callback:

    * The posted payload must confirm with the CallbackRequest schema.
    * The enrollment_id parameter must be well known to the employer.
      This is a kind of "correlation id" used to associate messages.
    * The provided key must be valid for that enrolment_id.
      This is a kind of shared-secret, set by the employer
      and shared with the training provider
      at the time the enrolment was sent to them.

    TODO:

    * we probably need to design "message" and "message-type" parameters.
    * this should probably return a unique callback_id (assigned by the API).
      Not sure why but we have it, maybe it will be useful to the sender.
      Maybe also return our wall-clock timestamp.
    * add "sender's temporal scope" parameter - used by employer
      to sort in the order of sender's intent.
    * Document idempotency; If we have this already,
      we respond as though this is the first time we ever saw it.
      Astute repeat senders may notice the wall-clock is a bit odd.
    '''
    callback_repo = S3CallbackRepo()
    use_case = CreateNewCallback(callback_repo=callback_repo)
    response = use_case.execute(inputs)

    return response
