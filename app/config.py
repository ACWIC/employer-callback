import functools
import logging
from typing import Optional

from pydantic import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


class Settings(BaseSettings):
    S3_ACCESS_KEY_ID: Optional[str]
    S3_SECRET_ACCESS_KEY: Optional[str]
    S3_ENDPOINT_URL: Optional[str]
    ENROLMENT_BUCKET: str
    CALLBACK_BUCKET: str

    @functools.cached_property
    def s3_configuration(self) -> dict:
        """
        Returns a dict of S3 configurations

        In managed AWS infrastructure like lambda, there's no need to provide
        these credentials.
        We encapsulate these details here, and expect the user to never call
        the AWS env variables directly.

        For simplicity, we assume that if the ACCESS KEY is not provided, there's
        nothing else provided.
        This behaviour can be changed if the need arises.
        """
        if not self.S3_ACCESS_KEY_ID:
            logger.info(
                "AWS config vars empty - assuming Environment is already authenticated"
            )
            return {}
        return {
            "aws_access_key_id": self.S3_ACCESS_KEY_ID,
            "aws_secret_access_key": self.S3_SECRET_ACCESS_KEY,
            "endpoint_url": self.S3_ENDPOINT_URL,
        }

    class Config:
        env_file = ".envs/.local/.sls"
        # for details about keep_untouched, see
        # https://github.com/samuelcolvin/pydantic/issues/1241
        keep_untouched = (functools.cached_property,)


settings = Settings()
