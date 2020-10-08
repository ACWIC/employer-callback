from fastapi import APIRouter

from app.repositories.s3_callback_repo import S3CallbackRepo
from app.requests.callback_requests import CallbackRequest
from app.use_cases.create_new_callback import CreateNewCallback

router = APIRouter()


@router.post("/callbacks")
def create_callback(inputs: CallbackRequest):
    """Message from Training Provider to Employer.

    Contains information about the delivery of training services,
    is linked to student identity and employer context by enrolment_id.

    POSTing a callback is a synchronous proccess
    that immediately succeeds (or fails).

    The API validates the callback:

    * The posted *payload* must confirm with the CallbackRequest schema.
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

    TODO:

    * we probably need to design a "message-type" attribute
      (to the CallbackRequest, i.e. sent with the POST).
      This could be used to identify the schema
      against which the payload could be validated.
      It could also be used by the recipient
      to process the data that is sent to them.
    * Currently, the "payload" is a dictionary
      (list of key/value pairs).
      Probably better for it to be a base64 encoded string,
      which would support arbitrary message-types in the future.
    * Document idempotency; If we have this already,
      we respond as though this is the first time we ever saw it.
      Astute repeat senders may notice the wall-clock is a bit odd.
      Error unless the message-type (when it exists),
      enrolment_id, payload and tp_sequence match.
      The service will always return the same values
      for recipient-assigned fields (callback_id, received).
    """
    callback_repo = S3CallbackRepo()
    use_case = CreateNewCallback(callback_repo=callback_repo)
    response = use_case.execute(inputs)

    return response
