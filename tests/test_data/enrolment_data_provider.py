import datetime

from app.domain.entities.callback import Callback
from app.domain.entities.enrolment import Enrolment
from app.utils.random import Random


class DataProvider:
    sample_enrolment: Enrolment
    sample_callback: Callback

    internal_reference = "ref1"
    ref_hash = Random.get_str_hash(internal_reference)
    sample_uuid = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    enrolment_id = "2dad3dd8-af28-4e61-ae23-4c93a456d10e"
    enrolment_id1 = "3dad3dd8-af28-4e61-ae23-4c93a456d10f"
    callback_id = "4dad3dd8-af28-4e61-ae23-4c93a456d10e"
    callback_id1 = "5dad3dd8-af28-4e61-ae23-4c93a456d10f"
    shared_secret = "6dad3dd8-af28-4e61-ae23-4c93a456d10e"
    course_id = "7dad3dd8-af28-4e61-ae23-4c93a456d10e"
    employee_id = "8dad3dd8-af28-4e61-ae23-4c93a456d10e"
    date_time_str = "2018-05-29 08:15:27.243860"
    date_time_str1 = "2018-06-29 08:15:27.243860"
    received = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
    received1 = datetime.datetime.strptime(date_time_str1, "%Y-%m-%d %H:%M:%S.%f")
    created = received
    crete_enrolment_response = {
        "enrolment_id": sample_uuid,
        "shared_secret": sample_uuid,
        "ref_hash": ref_hash,
    }
    enrolment_status = {
        "status": {
            "total_callbacks": "1",
            "most_recent_callback": str(received),
        }
    }
    enrolment_status1 = {
        "status": {
            "total_callbacks": "2",
            "most_recent_callback": str(received1),
        }
    }
    callbacks_list = {
        "callbacks_list": [{"callback_id": callback_id, "received": received}]
    }
    callbacks_list1 = {
        "callbacks_list": [
            {"callback_id": callback_id, "received": received},
            {"callback_id": callback_id, "received": received1},
        ]
    }
    callbacks_list1_json = {
        "callbacks_list": [
            {
                "callback_id": callback_id,
                "received": received.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            },
            {
                "callback_id": callback_id,
                "received": received1.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            },
        ]
    }

    def __init__(self):
        self.sample_enrolment = Enrolment(
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            internal_reference=self.ref_hash,
            created=self.created,
        )

        self.sample_create_enrolment = Enrolment(
            enrolment_id=self.sample_uuid,
            shared_secret=self.sample_uuid,
            internal_reference=self.ref_hash,
            created=self.created,
        )

        self.sample_enrolment1 = Enrolment(
            enrolment_id=self.enrolment_id1,
            shared_secret=self.shared_secret,
            internal_reference=self.ref_hash,
            created=self.created,
        )

        self.sample_callback = Callback(
            callback_id=self.callback_id,
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            received=self.received,
            sender_sequence=1,
            message_type_version="test",
            structured_data=b"test data",
        )

        self.sample_callback1 = Callback(
            callback_id=self.callback_id1,
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            sender_sequence=1,
            message_type_version="test",
            structured_data=b"test data",
        )
