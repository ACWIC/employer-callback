import json
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.callback import Callback
from app.repositories.callback_repo import CallbackRepo
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.utils.error_handling import handle_s3_errors

enrolment_repo = S3EnrolmentRepo()


class S3CallbackRepo(CallbackRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with handle_s3_errors():
            self.s3 = boto3.client("s3", **settings.s3_configuration)

    def save_callback(self, callback: dict) -> Callback:
        with handle_s3_errors():
            cb = Callback(**callback)
            self.s3.put_object(
                Body=bytes(cb.json(), "utf-8"),
                Key=f"callbacks/{cb.enrolment_id}/{cb.callback_id}.json",
                Bucket=settings.CALLBACK_BUCKET,
            )

        return cb

    def get_callbacks_list(self, enrolment_id: str):
        # check if enrolment exists, it will raise error if it doesn't
        enrolment_repo.get_enrolment(enrolment_id)
        with handle_s3_errors():
            # get callbacks for enrolment id
            callbacks_objects_list = self.s3.list_objects(
                Bucket=settings.CALLBACK_BUCKET, Prefix="{}/".format(enrolment_id)
            )
        callbacks_list = []
        # If there have been 0 callbacks, the list should be empty.
        if "Contents" not in callbacks_objects_list:
            return {"callbacks_list": callbacks_list}
        with handle_s3_errors():
            # add callback_id and datetime in list
            for row in callbacks_objects_list["Contents"]:
                obj = self.s3.get_object(
                    Key=row["Key"], Bucket=settings.CALLBACK_BUCKET
                )
                callback = Callback(**json.loads(obj["Body"].read().decode()))
                callbacks_list.append(
                    {"callback_id": callback.callback_id, "received": callback.received}
                )
        return {"callbacks_list": callbacks_list}
