import json
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.enrolment import Enrolment
from app.repositories.enrolment_repo import EnrolmentRepo
from app.utils.error_handling import handle_s3_errors


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with handle_s3_errors():
            self.s3 = boto3.client("s3", **settings.s3_configuration)

    def get_enrolment(self, enrolment_id: str) -> Enrolment:
        with handle_s3_errors():
            obj = self.s3.get_object(
                Key=f"enrolments/{enrolment_id}.json",
                Bucket=settings.ENROLMENT_BUCKET,
            )
        enrolment = json.loads(obj["Body"].read().decode())
        enrolment = Enrolment(**enrolment)
        return enrolment
