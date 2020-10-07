from pydantic import BaseModel
from app.repositories.callback_repo import CallbackRepo
from app.requests.callback_requests import CallbackRequest
from app.responses import ResponseFailure
from app.responses import ResponseSuccess


class CreateNewCallback(BaseModel):
    callback_repo: CallbackRepo  # class attribute (singleton)

    class Config:
        # Pydantic will complain if something (enrolment_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, request: CallbackRequest):
        try:
            # TODO: validate enrolment_id
            # TODO: validate key for enrolment_id
            # TODO: validate shared_secret key
            self.validate_enrolment_id(request)
            if request.invalid:
                raise Exception(f"Resource Error! {request.invalid['enrolment_id']}")
            self.validate_shared_secret(request)
            if request.invalid:
                raise Exception(f"Resource Error! {request.invalid['shared_secret']}")

            callback = self.callback_repo.save_callback(
                enrolment_id=request.enrolment_id,
                key=request.key,
                tp_sequence=request.tp_sequence,
                payload=request.payload
            )
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=callback)

    def validate_enrolment_id(self, request: CallbackRequest):
        # if the enrolment_id doesn't exist
        if request.enrolment_id != "dummy_enrolment_id":
            error_message = "'enrolment_id' doesn't exist!"
            request.invalid["enrolment_id"] = error_message

    def validate_shared_secret(self, request: CallbackRequest):
        # if the shared_secret doesn't match
        if request.key != "dummy_enrolment_key":
            error_message = "'shared_secret' doesn't match"
            request.invalid["shared_secret"] = error_message
