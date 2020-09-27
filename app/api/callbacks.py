from fastapi import APIRouter
from app.requests.callback_requests import NewCallbackRequest
from app.repositories.s3_callback_repo import S3CallbackRepo
from app.use_cases.create_new_callback import CreateNewCallback


router = APIRouter()


@router.post("/callbacks")
def create_callback(inputs: NewCallbackRequest):
    ''' Posting a callback is a synchronous proccess that
        immediately succeeds (or fails).

    TODO: the callback needs a enrollmentID
    TODO: validate the enrollmentID
    TODO: validate the keys/sig (Auth)
    TODO: draft schema, and validate against it
    '''
    callback_repo = S3CallbackRepo()
    use_case = CreateNewCallback(callback_repo=callback_repo)
    response = use_case.execute(inputs)

    return response
