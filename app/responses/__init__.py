from enum import Enum

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse


class SuccessType(int, Enum):
    SUCCESS = 200
    CREATED = 201


class FailureType(int, Enum):
    PARAMETER_ERROR = 400
    UNAUTHORISED_ERROR = 401
    RESOURCE_ERROR = 404
    VALIDATION_ERROR = 422
    SYSTEM_ERROR = 500


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

    @classmethod
    def build_from_validation_error(cls, message=None):
        return cls(
            type=FailureType.VALIDATION_ERROR, message=cls._format_message(message)
        )

    @classmethod
    def build_from_unauthorised_error(cls, message=None):
        return cls(
            type=FailureType.UNAUTHORISED_ERROR, message=cls._format_message(message)
        )


class ResponseSuccess(BaseModel):
    value: dict
    type: SuccessType = SuccessType.SUCCESS
    message: str = "Success"

    def __bool__(self):
        return True

    def build(self):
        content = jsonable_encoder(
            {"value": self.value, "message": self.message, "type": self.type}
        )
        return JSONResponse(content=content, status_code=self.type.value)
