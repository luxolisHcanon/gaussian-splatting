import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    SQS_QUEUE_URL: str = os.getenv("SQS_QUEUE_URL")
