from pydantic import BaseModel

from app.repositories.callback_repo import CallbackRepo
from app.repositories.s3_enrolment_repo import EnrolmentRepo
from app.requests.callback_requests import CallbackRequest
from app.responses import ResponseFailure, ResponseSuccess


class CreateNewCallback(BaseModel):
    callback_repo: CallbackRepo  # class attribute (singleton)
    enrolment_repo: EnrolmentRepo

    class Config:
        # Pydantic will complain if something (enrolment_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, request: CallbackRequest):
        try:
            enrolment_object = self.enrolment_repo.get_enrolment(
                enrolment_id=request.enrolment_id
            )
            # If request isn't failed, then an Enrolment object is returned, check shared_secret
            if enrolment_object.shared_secret != request.shared_secret:
                return ResponseFailure.build_from_unauthorised_error(
                    message="'shared_secret' key doesn't match"
                )
            callback = self.callback_repo.save_callback(request)
            message = "The callback has been saved."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=callback, message=message)
