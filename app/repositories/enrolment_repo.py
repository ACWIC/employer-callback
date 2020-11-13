import abc

from app.domain.entities.enrolment import Enrolment


class EnrolmentRepo(abc.ABC):
    @abc.abstractmethod
    def get_enrolment(self, enrolment_id: str) -> Enrolment:
        """"""
