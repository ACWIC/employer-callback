from typing import List

from pydantic import BaseModel


class InvalidRequestMessage(BaseModel):
    parameter: str
    message: str


class InvalidRequest(BaseModel):
    errors: List[InvalidRequestMessage] = []

    def add_error(self, parameter: str, message: str):
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __bool__(self) -> bool:
        return False


class ValidRequest(BaseModel):
    def __bool__(self) -> bool:
        return True
