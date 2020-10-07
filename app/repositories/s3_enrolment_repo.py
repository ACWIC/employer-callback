import os
import boto3
from datetime import datetime
from typing import Any
import uuid
from app.repositories.enrolment_repo import EnrolmentRepo
from app.domain.entities.enrolment import Enrolment

connection_data = {
    'aws_access_key_id': os.environ.get(
        'S3_ACCESS_KEY_ID',
    ) or None,
    'aws_secret_access_key': os.environ.get(
        'S3_SECRET_ACCESS_KEY',
    ) or None,
    'endpoint_url': os.environ.get(
        'S3_ENDPOINT_URL',
        'https://s3.us-east-1.amazonaws.com'
    )
}

enrolment_bucket = os.environ.get("ENROLMENT_BUCKET") or None


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3 = boto3.client('s3', **connection_data)

    def get_enrolment_by_id(self,  enrolment_id) -> Enrolment:
        try:
            enrolment_obj = self.s3.get_object(
                Bucket=enrolment_bucket,
                Key=enrolment_id,
            )
            if not isinstance(enrolment_obj, Enrolment):
                print(f"Wrong type! {type(enrolment_obj)}")
                raise Exception(f"Wrong type! {type(enrolment_obj)}")
            return enrolment_obj
        except Exception as e:
            print(f"Error! Message: {e}")
