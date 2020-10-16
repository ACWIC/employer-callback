from datetime import datetime

from pydantic import BaseModel


class Enrolment(BaseModel):
    created: datetime
    enrolment_id: str
    shared_secret: str
    internal_reference: str
