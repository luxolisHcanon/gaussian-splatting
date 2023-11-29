import os
from pydantic-settings import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()


class Config(BaseSettings):
    SQS_QUEUE_URL: str = os.getenv("SQS_QUEUE_URL")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET")


@lru_cache()
def get_config():
    return Config()
