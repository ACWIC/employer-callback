import datetime

from app.domain.entities.callback import Attachment, Callback
from app.domain.entities.enrolment import Enrolment
from app.requests.callback_requests import CallbackRequest


class CallbackDataProvider:  # (BaseModel):
    sample_callback: Callback
    sample_callback_2: Callback
    sample_callback_dict: dict

    sample_callback_request: CallbackRequest
    sample_invalid_callback_request: CallbackRequest

    sample_enrolment: Enrolment

    callback_id: str
    received: datetime
    enrolment_id: str
    shared_secret: str
    invalid_shared_secret: str
    internal_reference: str

    def __init__(self):
        self.callback_id = "063c3fa8-5887-4cac-858e-fb6bf197215f"
        self.callback_id_2 = "b16f2b51-d4e9-4ed7-b5f0-3ad40a107239"
        self.received = datetime.datetime(2020, 10, 21, 16, 56, 21, 829226)
        self.received_str = str(datetime.datetime(2020, 10, 21, 16, 56, 21, 829226))
        self.received_2 = datetime.datetime(2020, 10, 22, 16, 56, 21, 829226)
        self.received_str_2 = str(datetime.datetime(2020, 10, 22, 16, 56, 21, 829226))
        self.enrolment_id = "eec43c8c-e32d-4c90-8eae-99ebcc76671a"
        self.shared_secret = "2c2b38cc-da04-4c55-8604-8869abed42d4"
        self.invalid_shared_secret = "791fa918-2897-48b9-8be8-fcc9262bf947"
        self.internal_reference = "dummy_ref"

        self.sample_callback = Callback(
            callback_id=self.callback_id,
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            received=self.received,
            sender_sequence=0,
            message_type_version="test",
            structured_data=b"eyJ0ZXN0IjogImRhdGEifQ==",  # byte of '{"test": "data"}'
        )
        self.sample_callback_2 = Callback(
            callback_id=self.callback_id_2,
            enrolment_id=self.enrolment_id,
            shared_secret=self.invalid_shared_secret,
            received=self.received_2,
            sender_sequence=1,
            message_type_version="test",
            structured_data=b"test data",
        )
        self.attachment = Attachment.from_dict(
            {"content": b"test_data", "name": "dummy.txt"}
        )
        self.sample_callback_with_attachment = Callback(
            callback_id=self.callback_id,
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            received=self.received,
            sender_sequence=0,
            message_type_version="test",
            structured_data=b"eyJ0ZXN0IjogImRhdGEifQ==",  # byte of '{"test": "data"}'
            attachments=[self.attachment],
        )
        self.sample_callback_dict = self.sample_callback.dict()
        self.sample_get_callback_list = {"callbacks_list": [self.sample_callback]}
        self.sample_empty_callback_list = {"callbacks_list": []}

        self.sample_callback_request = CallbackRequest(
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            sender_sequence=0,
            message_type_version="test",
            structured_data={"test": "data"},
        )
        self.sample_callback_request_with_attachment = CallbackRequest(
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            sender_sequence=0,
            message_type_version="test",
            structured_data={"test": "data"},
            attachments=[self.attachment],
        )
        self.sample_invalid_callback_request = CallbackRequest(
            enrolment_id=self.enrolment_id,
            shared_secret=self.invalid_shared_secret,
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
