from pydantic import BaseModel

from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import ResponseFailure, ResponseSuccess


class GetEnrolmentStatus(BaseModel):
    enrolment_repo: EnrolmentRepo

    class Config:
        arbitrary_types_allowed = True

    def execute(self, enrolment_id: str):
        try:
            enrolment_status = self.enrolment_repo.get_enrolment_status(
                enrolment_id=enrolment_id
            )
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolment_status)
