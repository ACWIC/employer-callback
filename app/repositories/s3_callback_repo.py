import json
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

    def save_callback(self, callback: dict) -> Callback:
        try:
            cb = Callback(**callback)
            self.s3.put_object(
                Body=bytes(cb.json(), "utf-8"),
                Key=f"callbacks/{cb.enrolment_id}/{cb.callback_id}.json",
                Bucket=settings.CALLBACK_BUCKET,
            )
        except Exception as exception:
            raise exception

        return cb

    def get_callbacks_list(self, enrolment_id: str):
        from app.repositories.s3_enrolment_repo import S3EnrolmentRepo

        enrolment_repo = S3EnrolmentRepo()
        # check if enrolment exists, it will raise error if it doesn't
        enrolment_repo.get_enrolment(enrolment_id)
        try:
            # get callbacks for enrolment id
            callbacks_objects_list = self.s3.list_objects(
                Bucket=settings.CALLBACK_BUCKET, Prefix="{}/".format(enrolment_id)
            )
        except Exception as exception:
            raise exception
        # print("callbacks_objects_list", callbacks_objects_list)
        callbacks_list = []
        # If there have been 0 callbacks, the list should be empty.
        if "Contents" not in callbacks_objects_list:
            return {"callbacks_list": callbacks_list}
        # add callback_id and datetime in list
        for row in callbacks_objects_list["Contents"]:
            obj = self.s3.get_object(Key=row["Key"], Bucket=settings.CALLBACK_BUCKET)
            callback = Callback(**json.loads(obj["Body"].read().decode()))
            callbacks_list.append(
                {"callback_id": callback.callback_id, "received": callback.received}
            )
        # print("callbacks_list:", [callbacks_list])
        return {"callbacks_list": callbacks_list}
