import abc


class CallbackRepo(abc.ABC):

    @abc.abstractmethod
    def save_callback(self, callback_id, enrolment_id, key) -> None:
        pass
