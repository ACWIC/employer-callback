from enum import Enum
from uuid import UUID
from pydantic import BaseModel


class EnrolmentStatus(str, Enum):
    lodged = 'Lodged'


class EnrolmentAuthorisation(BaseModel):
    uuid: UUID
    course_id: str
    student_id: str
    status: EnrolmentStatus = EnrolmentStatus.lodged
