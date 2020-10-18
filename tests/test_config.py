from app.config import Settings


def test_s3_config_returns_empty_dict_when_aws_key_is_not_provided():
    settings = Settings(
        S3_ACCESS_KEY_ID=None, S3_SECRET_ACCESS_KEY=None, S3_ENDPOINT_URL=None
    )
    assert settings.s3_configuration == {}


def test_s3_config_returns_correct_settings_when_env_vars_exist():
    settings = Settings(
        S3_ACCESS_KEY_ID="key_id",
        S3_SECRET_ACCESS_KEY="secret_key",
        S3_ENDPOINT_URL="s3.com",
    )

    assert settings.s3_configuration == {
        "aws_access_key_id": "key_id",
        "aws_secret_access_key": "secret_key",
        "endpoint_url": "s3.com",
    }
