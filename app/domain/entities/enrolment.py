from datetime import datetime

from pydantic import BaseModel


class NewEnrolment(BaseModel):
    enrolment_id: str


class NewEnrolmentSecret(BaseModel):
    shared_secret: str


class Enrolment(BaseModel):
    enrolment_id: str
    shared_secret: str
    internal_reference: str
    created: datetime
