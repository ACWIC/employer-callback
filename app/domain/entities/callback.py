from enum import Enum
from uuid import UUID
from pydantic import BaseModel


class Callback(BaseModel):
    callback_id: UUID
    enrolment_id: str
    key: str
    # TODO: multiple things to add here
    # grep for TODO elseware :)
    # this is the documented model
