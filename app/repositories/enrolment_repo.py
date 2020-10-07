import abc

from app.domain.entities.enrolment import Enrolment


class EnrolmentRepo(abc.ABC):

    @abc.abstractmethod
    def get_enrolment_by_id(self,  enrolment_id) -> Enrolment:
        pass
