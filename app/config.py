import os


def get_envar(k, required=True):
    val = os.environ.get(k, None)
    if not val and required:
        msg = "{0} not supplied".format(k)
        exit(msg)
    return val


class Config(object):
    S3_ACCESS_KEY_ID = get_envar("S3_ACCESS_KEY_ID")
    S3_SECRET_ACCESS_KEY = get_envar("S3_SECRET_ACCESS_KEY")
    S3_ENDPOINT_URL = get_envar("S3_ENDPOINT_URL")
    ENROLMENT_BUCKET = get_envar("ENROLMENT_BUCKET")
