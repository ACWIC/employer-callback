import json
from datetime import datetime
from io import BytesIO

from fastapi.encoders import jsonable_encoder


def get_object_response(obj):
    """Returns a proper response for S3.client.get_object method"""
    obj = json.dumps(jsonable_encoder(obj.dict()), indent=2).encode("utf-8")
    output = BytesIO()
    output.write(obj)
    return {
        "Body": output,
        "DeleteMarker": True,
        "AcceptRanges": "string",
        "Expiration": "string",
        "Restore": "string",
        "LastModified": datetime(2015, 1, 1),
        "ContentLength": 123,
        "ETag": "string",
        "MissingMeta": 123,
        "VersionId": "string",
        "CacheControl": "string",
        "ContentDisposition": "string",
        "ContentEncoding": "string",
        "ContentLanguage": "string",
        "ContentRange": "string",
        "ContentType": "string",
        "Expires": datetime(2015, 1, 1),
        "WebsiteRedirectLocation": "string",
        "ServerSideEncryption": "AES256",
        "Metadata": {"string": "string"},
        "SSECustomerAlgorithm": "string",
        "SSECustomerKeyMD5": "string",
        "SSEKMSKeyId": "string",
        "StorageClass": "STANDARD",
        "RequestCharged": "requester",
        "ReplicationStatus": "COMPLETE",
        "PartsCount": 123,
        "TagCount": 123,
        "ObjectLockMode": "GOVERNANCE",
        "ObjectLockRetainUntilDate": datetime(2015, 1, 1),
        "ObjectLockLegalHoldStatus": "ON",
    }


def list_objects_response(list_of_keys):
    response = {
        "IsTruncated": True,
        "Marker": "string",
        "NextMarker": "string",
        "Contents": [],
        "Name": "string",
        "Prefix": "string",
        "Delimiter": "string",
        "MaxKeys": 123,
        "CommonPrefixes": [
            {"Prefix": "string"},
        ],
        "EncodingType": "url",
    }
    for key in list_of_keys:
        response["Contents"].append(
            {
                "Key": key,
                "LastModified": datetime(2015, 1, 1),
                "ETag": "string",
                "Size": 123,
                "StorageClass": "STANDARD",
                "Owner": {"DisplayName": "string", "ID": "string"},
            },
        )
    return response


def list_objects_empty_response():
    response = {
        "IsTruncated": True,
        "Marker": "string",
        "NextMarker": "string",
        "Name": "string",
        "Prefix": "string",
        "Delimiter": "string",
        "MaxKeys": 123,
        "CommonPrefixes": [
            {"Prefix": "string"},
        ],
        "EncodingType": "url",
    }
    return response
