from pydantic import BaseModel

from app.repositories.callback_repo import CallbackRepo
from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import ResponseFailure, ResponseSuccess


class GetEnrolmentStatus(BaseModel):
    enrolment_repo: EnrolmentRepo
    callback_repo: CallbackRepo

    class Config:
        arbitrary_types_allowed = True

    def execute(self, enrolment_id: str):
        try:
            callbacks_list = self.callback_repo.get_callbacks_list(enrolment_id)
            enrolment_status = self.enrolment_repo.get_enrolment_status(
                enrolment_id=enrolment_id, callbacks_list=callbacks_list
            )
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolment_status).build()
