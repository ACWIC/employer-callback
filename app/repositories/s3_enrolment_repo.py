import json
from typing import Any, Union

import boto3

from app.config import settings
from app.domain.entities.enrolment import Enrolment
from app.repositories.enrolment_repo import EnrolmentRepo
from app.utils.error_handling import handle_s3_errors
from app.utils.random import Random


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with handle_s3_errors():
            self.s3 = boto3.client("s3", **settings.s3_configuration)

    def save_enrolment(self, enrollment: dict):

        enrl = Enrolment(**enrollment)
        ref_hash = Random.get_str_hash(enrl.internal_reference)
        with handle_s3_errors():
            self.s3.put_object(
                Body=bytes(enrl.enrolment_id, "utf-8"),
                Key=f"employer_reference/{ref_hash}/enrolment_id.json",
                Bucket=settings.ENROLMENT_BUCKET,
            )

            self.s3.put_object(
                Body=bytes(enrl.json(), "utf-8"),
                # Body=bytes(enrl.shared_secret, "utf-8"),
                Key=f"enrolments/{enrl.enrolment_id}.json",
                Bucket=settings.ENROLMENT_BUCKET,
            )

        return enrl

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

    def get_enrolment(self, enrolment_id: str):
        print(
            "get_enrolment() enrolment_id, BUCKET",
            enrolment_id,
            settings.ENROLMENT_BUCKET,
        )
        with handle_s3_errors():
            obj = self.s3.get_object(
                Key=f"enrolments/{enrolment_id}.json", Bucket=settings.ENROLMENT_BUCKET
            )
            enrolment = Enrolment(**json.loads(obj["Body"].read().decode()))
            return enrolment

    def get_enrolment_status(self, enrolment_id: str, callbacks_list: list):
        total_callbacks = len(callbacks_list["callbacks_list"])
        most_recent_callback = ""
        for row in callbacks_list["callbacks_list"]:
            most_recent_callback = row["received"]

        enrolment = {
            "status": {
                "total_callbacks": str(total_callbacks),
                "most_recent_callback": str(most_recent_callback),
            }
        }
        return enrolment
