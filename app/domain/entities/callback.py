from datetime import datetime

from pydantic import BaseModel


class Callback(BaseModel):
    callback_id: str
    enrolment_id: str
    shared_secret: str
    received: datetime
    tp_sequence: int
    payload: dict

    def to_dict(self):
        return vars(self)

    def __eq__(self, obj):
        ignored = ["callback_id", "received"]
        d1 = self.to_dict()
        d2 = obj.to_dict()
        for k1, v1 in d1.items():
            if k1 not in ignored and (k1 not in d2 or d2[k1] != v1):
                return False
        return True
