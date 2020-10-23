from datetime import datetime

from pydantic import BaseModel

from app.repositories.enrolment_repo import EnrolmentRepo
from app.requests.enrolment_requests import NewEnrolmentRequest
from app.responses import ResponseFailure, ResponseSuccess
from app.utils import Random


class CreateNewEnrolment(BaseModel):
    enrolment_repo: EnrolmentRepo

    class Config:
        # Pydantic will complain if something (enrolment_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, request: NewEnrolmentRequest):

        internal_reference = request.internal_reference
        if not self.enrolment_repo.is_reference_unique(
            Random.get_str_hash(internal_reference)
        ):
            return ResponseFailure.validation_error(
                message=f"internal_reference {internal_reference} is already used."
            )

        params = {
            "enrolment_id": Random.get_uuid(),
            "shared_secret": Random.get_uuid(),
            "internal_reference": internal_reference,
            "created": datetime.now(),
        }

        try:
            enrolment = self.enrolment_repo.save_enrolment(params)
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolment).build()
