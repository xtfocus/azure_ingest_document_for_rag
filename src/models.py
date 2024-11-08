from typing import Dict, List

from loguru import logger
from pydantic import BaseModel


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
