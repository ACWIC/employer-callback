import os
from typing import Any

import boto3

from app.domain.entities.callback import Callback
from app.repositories.callback_repo import CallbackRepo

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


class S3CallbackRepo(CallbackRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3 = boto3.client("s3", **connection_data)

    def save_callback(self, callback: dict):
        cb = Callback(**callback)

        self.s3.put_object(
            Body=bytes(cb.json(), "utf-8"),
            Key=f"callbacks/{cb.enrolment_id}/{cb.callback_id}.json",
            Bucket=os.environ["CALLBACK_BUCKET"],
        )

        return cb
