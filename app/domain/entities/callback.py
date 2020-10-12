from datetime import datetime

from pydantic import BaseModel


class Callback(BaseModel):
    callback_id: str
    enrolment_id: str
    shared_secret: str
    received: datetime
    tp_sequence: int
    payload: dict
