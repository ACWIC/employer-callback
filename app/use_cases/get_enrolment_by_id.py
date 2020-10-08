from pydantic import BaseModel


class GetEnrolmentByID(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    def execute(self):
        # FIXME
        pass
