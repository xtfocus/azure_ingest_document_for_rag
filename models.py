import os
from dataclasses import dataclass
from typing import Dict, List

from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel

try:
    load_dotenv(".env.local")
    logger.info("ENV read")
except:
    pass


@dataclass
class ModelConfig:
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int = 4096
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 0.5
    api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
    api_key: str = os.getenv("AZURE_OPENAI_KEY", "")
    endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    model_deployment: str = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "")


class CustomSkillException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        logger.error(
            f"CustomSkillException raised: {self.message}"
        )  # Log exception on creation
        super().__init__(self.message)


class RequestData(BaseModel):
    values: List[Dict]
