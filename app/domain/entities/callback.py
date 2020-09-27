from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel


class Callback(BaseModel):
    callback_id: UUID
    received: datetime
    enrolment_id: str
    key: str
    tp_sequence: int
    payload: dict
