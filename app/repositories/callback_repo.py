import abc
from typing import List

from app.domain.entities.callback import Callback


class CallbackRepo(abc.ABC):
    @abc.abstractmethod
    def save_callback(self, callback: dict) -> (bool, Callback):
        """"""

    @abc.abstractmethod
    def is_callback_already_exists(self, callback: Callback):
        """"""

    @abc.abstractmethod
    def get_callbacks_list(self, enrolment_id: str) -> List[Callback]:
        """"""
