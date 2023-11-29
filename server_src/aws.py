from functools import lru_cache

import boto3

from . config import get_config


class S3Session:
    config = get_config()
    bucket_name = config.S3_BUCKET_NAME
    session = boto3.Session()
    s3_client = session.client("s3")
    s3_resource = boto3.resource("s3")


@lru_cache()
def get_s3_session():
    return S3Session()
