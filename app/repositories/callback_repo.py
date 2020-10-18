import abc
from typing import List

from app.domain.entities.callback import Callback


class CallbackRepo(abc.ABC):
    @abc.abstractmethod
    def save_callback(self, callback: dict) -> Callback:
        pass

    @abc.abstractmethod
    def get_callbacks_list(self, enrolment_id: str) -> List[Callback]:
        pass
