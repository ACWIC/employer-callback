from datetime import datetime

from pydantic import BaseModel


class Enrolment(BaseModel):
    created: datetime
    enrolment_id: str
    key: str
