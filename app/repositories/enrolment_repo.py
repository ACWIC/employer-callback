import abc

from app.config import settings
from app.domain.entities.callback import Callback
from app.domain.entities.enrolment import Enrolment


class EnrolmentRepo(abc.ABC):
    @abc.abstractmethod
    def create_enrolment(self, internal_reference: str) -> Enrolment:
        """"""

    @abc.abstractmethod
    def get_enrolment(self, enrolment_id: str) -> Enrolment:
        """"""

    @abc.abstractmethod
    def enrolment_exists(
        self, enrolment_id: str, bucket=settings.ENROLMENT_BUCKET
    ) -> bool:
        """"""

    @abc.abstractmethod
    def is_reference_unique(self, ref_hash: str) -> bool:
        """"""

    @abc.abstractmethod
    def get_enrolment_status(self, enrolment_id: str) -> dict:
        """"""

    @abc.abstractmethod
    def get_callbacks_list(self, enrolment_id: str) -> dict:
        """"""

    @abc.abstractmethod
    def get_callback(self, enrolment_id: str, callback_id: str) -> Callback:
        """"""
