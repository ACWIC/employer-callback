import json
import os
import uuid
from datetime import datetime
from typing import Any

import boto3

from app.domain.entities.callback import Callback
from app.domain.entities.enrolment import Enrolment
from app.repositories.enrolment_repo import EnrolmentRepo

connection_data = {
    "aws_access_key_id": os.environ.get(
        "S3_ACCESS_KEY_ID",
    )
    or None,
    "aws_secret_access_key": os.environ.get(
        "S3_SECRET_ACCESS_KEY",
    )
    or None,
    "endpoint_url": os.environ.get(
        "S3_ENDPOINT_URL", "https://s3.us-east-1.amazonaws.com"
    ),
}


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3 = boto3.client("s3", **connection_data)

    def save_enrolment(self, enrolment_id: str):
        enrl = Enrolment(
            enrolment_id=enrolment_id,
            key=str(uuid.uuid4()),  # random GUID
            created=datetime.now(),  # check the clock
        )
        self.s3.put_object(
            Body=bytes(enrl.json(), "utf-8"),
            Key=f"{enrl.enrolment_id}.json",
            Bucket=os.environ["ENROLMENT_BUCKET"],
        )
        return enrl

    def get_enrolment(self, enrolment_id: str):
        obj = self.s3.get_object(
            Key=f"{enrolment_id}.json", Bucket=os.environ["ENROLMENT_BUCKET"]
        )
        enrl = Enrolment(**json.loads(obj["Body"].read().decode()))
        return enrl

    def get_callbacks_list(self, enrolment_id: str):
        callbacks_list = []
        for row in self.s3.list_objects(
            Bucket=os.environ["CALLBACK_BUCKET"], Prefix="{}/".format(enrolment_id)
        )["Contents"]:
            obj = self.s3.get_object(
                Key=row["Key"], Bucket=os.environ["CALLBACK_BUCKET"]
            )
            cb = Callback(**json.loads(obj["Body"].read().decode()))
            if cb.enrolment_id == enrolment_id:
                callbacks_list.append(
                    {"callback_id": cb.callback_id, "received": cb.received}
                )
        print("callbacks_list:", [callbacks_list])
        return {"callbacks_list": callbacks_list}

    # Temp: For testing purpose
    def save_callback(
        self, enrolment_id: str, key: str, tp_sequence: int, payload: dict
    ):
        cb = Callback(
            callback_id=str(uuid.uuid4()),
            enrolment_id=enrolment_id,
            key=str(uuid.uuid4()),
            received=datetime.now(),
            tp_sequence=tp_sequence,
            payload=payload,
        )
        self.s3.put_object(
            Body=bytes(cb.json(), "utf-8"),
            Key=f"{cb.enrolment_id}/{cb.callback_id}.json",
            Bucket=os.environ["CALLBACK_BUCKET"],
        )
        return cb
