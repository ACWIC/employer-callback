import abc


class EnrolmentRepo(abc.ABC):
    @abc.abstractmethod
    def save_enrolment(self, enrollment: dict) -> None:
        pass

    @abc.abstractmethod
    def get_enrolment(self, enrolment_id: str) -> None:
        pass

    @abc.abstractmethod
    def get_enrolment_status(self, enrolment_id: str) -> None:
        pass
