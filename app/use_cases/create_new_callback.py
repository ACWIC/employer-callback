from pydantic import BaseModel
from app.repositories.callback_repo import CallbackRepo
from app.repositories.enrolment_repo import EnrolmentRepo
from app.requests.callback_requests import CallbackRequest
from app.responses import ResponseFailure
from app.responses import ResponseSuccess


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
            # TODO: validate enrolment_id
            # TODO: validate key for enrolment_id
            # TODO: validate shared_secret key
            enrolment_object = self.enrolment_repo.get_enrolment_by_id(request.enrolment_id)
            if not enrolment_object:
                return ResponseFailure.build_from_resource_error(message="'enrolment_id' doesn't exist!")
            if enrolment_object.key != request.key:
                return ResponseFailure.build_from_resource_error(message="'shared_secret' key doesn't match")

            callback = self.callback_repo.save_callback(
                enrolment_id=request.enrolment_id,
                key=request.key,
                tp_sequence=request.tp_sequence,
                payload=request.payload
            )
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=callback)
