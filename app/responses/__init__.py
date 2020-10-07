from enum import Enum

from pydantic import BaseModel
from pydantic.typing import Literal


class FailureType(str, Enum):
    RESOURCE_ERROR = "ResourceError"
    SYSTEM_ERROR = "SystemError"


class ResponseFailure(BaseModel):
    type: FailureType
    message: str

    @classmethod
    def _format_message(cls, message):
        if isinstance(message, Exception):
            return f"{message.__class__.__name__}: {message}"
        return message

    def __bool__(self):
        return False

    @classmethod
    def build_from_resource_error(cls, message=None):
        return cls(
            type=FailureType.RESOURCE_ERROR, message=cls._format_message(message)
        )

    @classmethod
    def build_from_system_error(cls, message=None):
        return cls(type=FailureType.SYSTEM_ERROR, message=cls._format_message(message))


class ResponseSuccess(BaseModel):
    type: Literal["Success"] = "Success"
    value: dict

    def __bool__(self):
        return True
