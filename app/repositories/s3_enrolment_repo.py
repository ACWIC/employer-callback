import os
import boto3
from typing import Any
import uuid
from app.repositories.enrolment_repo import EnrolmentRepo
from app.domain.entities.enrolment_authorisation import EnrolmentAuthorisation

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


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3 = boto3.client('s3', **connection_data)

    def save_enrolment(self, course_id, student_id):
        # Create a submission uuid
        enrolment = EnrolmentAuthorisation(
            uuid=uuid.uuid4(),
            course_id=course_id,
            student_id=student_id
        )

        # Write directory to bucket
        self.s3.put_object(
            Body=bytes(enrolment.json(), 'utf-8'),
            Key=f'{enrolment.uuid}.json',
            Bucket=os.environ['ENROLMENT_AUTHORISATION_BUCKET']
        )

        return enrolment
