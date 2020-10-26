from datetime import datetime

from pydantic import BaseModel


class Callback(BaseModel):
    callback_id: str
    enrolment_id: str
    shared_secret: str
    received: datetime
    tp_sequence: int
    payload: dict

    def __eq__(self, obj):
        exclude = {"callback_id", "received"}
        d1 = self.dict(exclude=exclude)
        d2 = obj.dict(exclude=exclude)
        return d1 == d2
