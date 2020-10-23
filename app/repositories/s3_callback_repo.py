import json
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.callback import CallbackEvent
from app.repositories.callback_repo import CallbackRepo
from app.requests.callback_requests import CallbackRequest


class S3CallbackRepo(CallbackRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.s3 = boto3.client("s3", **settings.s3_configuration)

    def save_callback(self, request: CallbackRequest) -> CallbackEvent:
        instance = CallbackEvent.from_request(request)
        self.s3.put_object(
            Body=instance.serialize(),
            Key=f"callbacks/{instance.enrolment_id}/{instance.uid}.json",
            Bucket=settings.CALLBACK_BUCKET,
        )

        return instance

    def get_callbacks_list(self, enrolment_id: str):
        print(
            "get_callbacks_list() enrolment_id, BUCKET",
            enrolment_id,
            settings.CALLBACK_BUCKET,
        )
        from app.repositories.s3_enrolment_repo import S3EnrolmentRepo

        enrolment_repo = S3EnrolmentRepo()
        # check if enrolment exists, it will raise error if it doesn't
        enrolment_repo.get_enrolment(enrolment_id)
        # get callbacks for enrolment id
        callbacks_objects_list = self.s3.list_objects(
            Bucket=settings.CALLBACK_BUCKET, Prefix="{}/".format(enrolment_id)
        )
        # print("callbacks_objects_list", callbacks_objects_list)
        callbacks_list = []
        # If there have been 0 callbacks, the list should be empty.
        if "Contents" not in callbacks_objects_list:
            return {"callbacks_list": callbacks_list}
        # add callback_id and datetime in list
        for row in callbacks_objects_list["Contents"]:
            obj = self.s3.get_object(Key=row["Key"], Bucket=settings.CALLBACK_BUCKET)
            callback = CallbackEvent(**json.loads(obj["Body"].read().decode()))
            callbacks_list.append(
                {"callback_id": callback.callback_id, "received": callback.received}
            )
        # print("callbacks_list:", [callbacks_list])
        return {"callbacks_list": callbacks_list}
