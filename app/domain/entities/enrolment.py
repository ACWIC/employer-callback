from uuid import UUID
from pydantic import BaseModel


class Enrolment(BaseModel):
    enrolment_id: UUID
    key: UUID
