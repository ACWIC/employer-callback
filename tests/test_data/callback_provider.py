import datetime

from app.domain.entities.callback import Callback
from app.domain.entities.enrolment import Enrolment
from app.requests.callback_requests import CallbackRequest


class CallbackDataProvider:  # (BaseModel):
    sample_callback: Callback
    sample_callback_2: Callback
    sample_callback_dict: dict

    sample_callback_request: CallbackRequest
    sample_invalid_callback_request: CallbackRequest
    sample_get_callback_list: dict
    sample_empty_callback_list: dict
    callback_repo_list: dict

    sample_enrolment: Enrolment

    callback_id: str
    tp_ref: int
    received: datetime
    payload: dict
    enrolment_id: str
    shared_secret: str
    invalid_shared_secret: str
    internal_reference: str

    def __init__(self):
        self.callback_id = "063c3fa8-5887-4cac-858e-fb6bf197215f"
        self.callback_id_2 = "b16f2b51-d4e9-4ed7-b5f0-3ad40a107239"
        self.tp_ref = 123456
        self.received = datetime.datetime(2020, 10, 21, 16, 56, 21, 829226)
        self.received_str = str(datetime.datetime(2020, 10, 21, 16, 56, 21, 829226))
        self.received_2 = datetime.datetime(2020, 10, 22, 16, 56, 21, 829226)
        self.received_str_2 = str(datetime.datetime(2020, 10, 22, 16, 56, 21, 829226))
        self.payload = {"data": "blbnjsd;fnbs"}
        self.enrolment_id = "eec43c8c-e32d-4c90-8eae-99ebcc76671a"
        self.shared_secret = "2c2b38cc-da04-4c55-8604-8869abed42d4"
        self.invalid_shared_secret = "791fa918-2897-48b9-8be8-fcc9262bf947"
        self.internal_reference = "dummy_ref"

        self.sample_callback = Callback(
            callback_id=self.callback_id,
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            tp_sequence=self.tp_ref,
            received=self.received,
            payload=self.payload,
            sender_sequence=0,
            message_type_version="test",
            structured_data=b"test data",
        )
        self.sample_callback_2 = Callback(
            callback_id=self.callback_id_2,
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            tp_sequence=self.tp_ref,
            received=self.received_2,
            payload=self.payload,
            sender_sequence=1,
            message_type_version="test",
            structured_data=b"test data",
        )
        self.sample_callback_dict = vars(self.sample_callback)
        self.sample_get_callback_list = {"callbacks_list": [self.sample_callback]}
        self.sample_empty_callback_list = {"callbacks_list": []}

        self.callback_repo_list = {
            "callbacks_list": [
                vars(self.sample_callback),
                vars(self.sample_callback_2),
            ]
        }

        self.sample_callback_request = CallbackRequest(
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            tp_sequence=self.tp_ref,
            payload=self.payload,
            sender_sequence=0,
            message_type_version="test",
            structured_data={"test": "data"},
        )
        self.sample_invalid_callback_request = CallbackRequest(
            enrolment_id=self.enrolment_id,
            shared_secret=self.invalid_shared_secret,
            tp_sequence=self.tp_ref,
            payload=self.payload,
            sender_sequence=1,
            message_type_version="test",
            structured_data={"test": "data"},
        )

        self.sample_enrolment = Enrolment(
            created=self.received,
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            internal_reference=self.internal_reference,
        )
