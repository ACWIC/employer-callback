import abc
from typing import List

from app.domain.entities.callback import Callback


class CallbackRepo(abc.ABC):
    @abc.abstractmethod
    def get_callback_from_cache(self, callback: Callback) -> Callback:
        """"""

    @abc.abstractmethod
    def save_callback(self, callback: dict) -> Callback:
        """"""

    @abc.abstractmethod
    def callback_exists(self, callback_obj: Callback) -> bool:
        """"""

    @abc.abstractmethod
    def get_callbacks_list(self, enrolment_id: str) -> List[Callback]:
        """"""
