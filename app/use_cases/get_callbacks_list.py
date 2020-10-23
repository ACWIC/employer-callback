from pydantic import BaseModel

from app.repositories.callback_repo import CallbackRepo
from app.responses import ResponseFailure, ResponseSuccess


class GetCallbacksList(BaseModel):
    callback_repo: CallbackRepo

    class Config:
        arbitrary_types_allowed = True

    def execute(self, enrolment_id: str):
        try:
            enrolment = self.callback_repo.get_callbacks_list(enrolment_id=enrolment_id)
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolment).build()
