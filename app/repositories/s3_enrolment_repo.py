import json
import uuid
from datetime import datetime
from typing import Any, Union

import boto3

from app.config import settings
from app.domain.entities.callback import Callback
from app.domain.entities.enrolment import Enrolment
from app.repositories.enrolment_repo import EnrolmentRepo
from app.utils.random import Random


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.params = {
            "aws_access_key_id": settings.S3_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.S3_SECRET_ACCESS_KEY,
            "endpoint_url": settings.S3_ENDPOINT_URL,
        }
        self.s3 = boto3.client("s3", **self.params)

    def save_enrolment(self, enrollment: dict):

        enrl = Enrolment(**enrollment)
        ref_hash = Random.get_str_hash(enrl.internal_reference)

        self.s3.put_object(
            Body=bytes(enrl.enrolment_id, "utf-8"),
            Key=f"employer_reference/{ref_hash}/enrolment_id.json",
            Bucket=settings.ENROLMENT_BUCKET,
        )

        self.s3.put_object(
            Body=bytes(enrl.shared_secret, "utf-8"),
            Key=f"enrolments/{enrl.enrolment_id}.json",
            Bucket=settings.ENROLMENT_BUCKET,
        )

        return enrl

    def get_enrolment(self, enrolment_id: str):
        obj = self.s3.get_object(
            Key=f"{enrolment_id}.json", Bucket=settings.ENROLMENT_BUCKET
        )
        enrl = Enrolment(**json.loads(obj["Body"].read().decode()))
        return enrl

    def get_callbacks_list(self, enrolment_id: str):
        callbacks_list = []
        for row in self.s3.list_objects(
            Bucket=settings.CALLBACK_BUCKET, Prefix="{}/".format(enrolment_id)
        )["Contents"]:
            obj = self.s3.get_object(Key=row["Key"], Bucket=settings.CALLBACK_BUCKET)
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
            Bucket=settings.CALLBACK_BUCKET,
        )
        return cb

    def is_reference_unique(
        self, ref_hash: str
    ) -> Union[bool, Enrolment]:  # TODO combine with get_enrolment
        """
        Check whether given internal_reference is unique or not
        """
        try:
            self.s3.get_object(
                Key=f"employer_reference/{ref_hash}/enrolment_id.json",
                Bucket=settings.ENROLMENT_BUCKET,
            )
        except Exception:
            return True
        else:
            return False
