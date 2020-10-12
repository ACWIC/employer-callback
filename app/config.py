from pydantic import BaseSettings


class Settings(BaseSettings):
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_ENDPOINT_URL: str
    ENROLMENT_BUCKET: str
    CALLBACK_BUCKET: str

    class Config:
        env_file = ".envs/.local/.sls"


settings = Settings()
