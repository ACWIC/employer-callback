from datetime import datetime

from pydantic import BaseModel


class Callback(BaseModel):
    callback_id: str
    received: datetime
    enrolment_id: str
    key: str
    tp_sequence: int
    payload: dict
