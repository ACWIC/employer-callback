import random
from datetime import datetime
from uuid import uuid4

from app.domain.entities.callback import Callback
from app.requests.callback_requests import CallbackRequest

dummy_callback_id = str(uuid4())
dummy_enrolment_id = str(uuid4())
dummy_invalid_enrolment_id = str(uuid4())
dummy_shared_secret = str(uuid4())
dummy_invalid_shared_secret = str(uuid4())
dummy_received = datetime.now()
dummy_ref = "dummy_ref"
dummy_tp_ref = random.randint(0, 99999)
dummy_payload = {"data": "blbnjsd;fnbs"}


class CallbackDataProvider:  # (BaseModel):
    sample_callback: Callback
    sample_callback_dict: dict
    sample_enrolment_id: str
    sample_get_callback_list: dict

    sample_callback_request: CallbackRequest
    sample_callback_request_dict: dict

    def __init__(self):
        self.enrolment_id = dummy_enrolment_id
        self.shared_secret = dummy_shared_secret
        self.internal_reference = dummy_ref
        # Course Sample
        self.sample_callback = Callback(
            callback_id=dummy_callback_id,
            enrolment_id=dummy_enrolment_id,
            shared_secret=dummy_shared_secret,
            tp_sequence=dummy_tp_ref,
            received=dummy_received,
            payload=dummy_payload,
        )
        self.sample_course_dict = vars(self.sample_callback)
        self.sample_get_callback_list = {"callbacks_list": [self.sample_callback]}

        self.sample_callback_request = CallbackRequest(
            enrolment_id=dummy_enrolment_id,
            shared_secret=dummy_shared_secret,
            tp_sequence=dummy_tp_ref,
            payload=dummy_payload,
        )
        self.sample_invalid_callback_request = CallbackRequest(
            enrolment_id=dummy_enrolment_id,
            shared_secret=dummy_invalid_shared_secret,
            tp_sequence=dummy_tp_ref,
            payload=dummy_payload,
        )
