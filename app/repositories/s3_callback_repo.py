import uuid
from datetime import datetime
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.callback import Callback
from app.repositories.callback_repo import CallbackRepo


class S3CallbackRepo(CallbackRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.params = {
            "aws_access_key_id": settings.S3_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.S3_SECRET_ACCESS_KEY,
            "endpoint_url": settings.S3_ENDPOINT_URL,
        }
        self.s3 = boto3.client("s3", **self.params)

    def save_callback(
        self, enrolment_id: str, key: str, tp_sequence: int, payload: dict
    ) -> Callback:

        cb = Callback(
            callback_id=uuid.uuid4(),
            enrolment_id=enrolment_id,
            key=key,
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
