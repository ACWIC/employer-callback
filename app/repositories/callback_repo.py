import abc

from app.domain.entities.callback import Callback


class CallbackRepo(abc.ABC):
    @abc.abstractmethod
    def save_callback(self, callback: dict) -> Callback:
        pass
