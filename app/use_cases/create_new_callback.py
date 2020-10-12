from pydantic import BaseModel

from app.repositories.callback_repo import CallbackRepo
from app.requests.callback_requests import CallbackRequest
from app.responses import ResponseFailure, ResponseSuccess


class CreateNewCallback(BaseModel):
    callback_repo: CallbackRepo  # class attribute (singleton)

    class Config:
        # Pydantic will complain if something (enrolment_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, request: CallbackRequest):
        params = {
            "enrolment_id": request.enrolment_id,
            "shared_secret": request.shared_secret,
            "tp_sequence": request.tp_sequence,
            "payload": request.payload,
        }
        try:
            # TODO: validate enrolment_id
            # TODO: validate key for enrolment_id
            callback = self.callback_repo.save_callback(params)
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=callback)
