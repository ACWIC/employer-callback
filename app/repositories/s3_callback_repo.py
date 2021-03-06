import json
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.callback import Callback
from app.repositories.callback_repo import CallbackRepo
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.callback_requests import CallbackRequest
from app.utils.error_handling import handle_s3_errors

enrolment_repo = S3EnrolmentRepo()


class S3CallbackRepo(CallbackRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with handle_s3_errors():
            self.s3 = boto3.client("s3", **settings.s3_configuration)
        # Cached objects
        self.callbacks = list()

    def get_callback_from_cache(self, callback_obj: Callback) -> Callback:
        for callback in self.callbacks:
            if callback == callback_obj:
                return callback
        # This line should be never reached
        return  # noqa

    def callback_exists(self, callback_obj: Callback) -> bool:
        with handle_s3_errors():
            callbacks = self.s3.list_objects(Bucket=settings.CALLBACK_BUCKET)
        if "Contents" not in callbacks:
            return False

        for row in callbacks["Contents"]:
            callback = self._get_object_from_s3(row)
            if callback == callback_obj:
                return True

        return False

    def save_callback(self, request: CallbackRequest) -> Callback:
        cb = Callback.from_request(request)
        if self.callback_exists(cb):
            cb = self.get_callback_from_cache(cb)
        else:
            with handle_s3_errors():
                self.s3.put_object(
                    Body=bytes(cb.json(), "utf-8"),
                    Key=f"callbacks/{cb.enrolment_id}/{cb.callback_id}.json",
                    Bucket=settings.CALLBACK_BUCKET,
                )
        return cb

    def _get_object_from_s3(self, data):
        with handle_s3_errors():
            obj = self.s3.get_object(Key=data["Key"], Bucket=settings.CALLBACK_BUCKET)
        callback = Callback(**json.loads(obj["Body"].read().decode()))
        # Add fetched object to cache
        if callback not in self.callbacks:
            self.callbacks.append(callback)
        return callback
