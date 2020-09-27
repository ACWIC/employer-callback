import abc


class EnrolmentRepo(abc.ABC):

    @abc.abstractmethod
    def save_enrolment(self, course_id: str, student_id: str) -> None:
        pass
