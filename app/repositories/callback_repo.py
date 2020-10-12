import abc


class CallbackRepo(abc.ABC):
    @abc.abstractmethod
    def save_callback(self, callback: dict) -> None:
        pass
