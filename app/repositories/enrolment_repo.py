import abc


class EnrolmentRepo(abc.ABC):
    @abc.abstractmethod
    def save_enrolment(self, enrolment_id: dict) -> None:
        """"""

    @abc.abstractmethod
    def get_enrolment(self, enrolment_id: str) -> None:
        """"""

    @abc.abstractmethod
    def get_callbacks_list(self, enrolment_id: str) -> None:
        """"""

    # Temp: For testing purpose
    @abc.abstractmethod
    def save_callback(
        self, enrolment_id: str, key: str, tp_sequence: int, payload: dict
    ) -> None:
        """"""
