import abc

from app.domain.entities.callback import Callback


class CallbackRepo(abc.ABC):
    @abc.abstractmethod
    def save_callback(
        self, enrolment_id: str, key: str, tp_sequence: int, payload: dict
    ) -> Callback:
        pass
