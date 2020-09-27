from enum import Enum
from uuid import UUID
from pydantic import BaseModel


class Callback(BaseModel):
    uuid: UUID
    # TODO: multiple things to add here
    # grep for TODO elseware :)
