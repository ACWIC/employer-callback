from pydantic import BaseModel

from app.repositories.enrolment_repo import EnrolmentRepo
from app.requests.enrolment_requests import NewEnrolmentRequest
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class CreateNewEnrolment(BaseModel):
    enrolment_repo: EnrolmentRepo

    class Config:
        # Pydantic will complain if something (enrolment_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, request: NewEnrolmentRequest):

        try:
            # No two enrolments may use the same internal_reference,
            # for the same employer
            if not self.enrolment_repo.is_reference_unique(request.internal_reference):
                return ResponseFailure.build_from_validation_error(
                    message="internal_reference "
                    + request.internal_reference
                    + " is already used."
                )
            enrolment = self.enrolment_repo.create_enrolment(request.internal_reference)
            code = SuccessType.CREATED
            message = "The enrolment has been created."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolment, message=message, type=code)
