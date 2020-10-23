import abc

from app.domain.entities.callback import CallbackEvent


class CallbackRepo(abc.ABC):
    @abc.abstractmethod
    def save_callback(self, callback: dict) -> CallbackEvent:
        pass
