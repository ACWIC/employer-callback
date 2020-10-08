from pydantic import BaseModel

from app.repositories.enrolment_repo import EnrolmentRepo
from app.requests.enrolment_requests import NewEnrolmentRequest
from app.responses import ResponseFailure, ResponseSuccess


class CreateNewEnrolment(BaseModel):
    enrolment_repo: EnrolmentRepo  # class attribute (singleton)

    class Config:
        # Pydantic will complain if something (enrolment_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, request: NewEnrolmentRequest):

        try:
            enrolment = self.enrolment_repo.save_enrolment(
                enrolment_id=request.enrolment_id,
            )
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolment)
