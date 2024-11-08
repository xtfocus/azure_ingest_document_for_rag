import os
from enum import Enum
from typing import Any, Dict, List

from loguru import logger

from .models import CustomSkillException


class ScenarioType(Enum):

    SUMMARIZATION = "summarization"
    ENTITY_RECOGNITION = "entity-recognition"
    IMAGE_CAPTIONING = "image-captioning"
    IMAGE_DESCRIPTION = "image-description"


def prepare_messages(
    request_body: Dict, scenario: str, custom_prompts: Dict
) -> List[Dict]:
    """Prepare messages based on scenario type"""

    messages = []

    system_prompt = custom_prompts.get(scenario)

    if not system_prompt:
        raise ValueError(f"System prompt not found for {scenario}")

    if scenario == ScenarioType.SUMMARIZATION.value:

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request_body["data"]["text"]},
        ]

    elif scenario == ScenarioType.ENTITY_RECOGNITION.value:

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request_body["data"]["text"]},
        ]

    elif scenario in [
        ScenarioType.IMAGE_CAPTIONING.value,
        ScenarioType.IMAGE_DESCRIPTION.value,
    ]:

        image_data = request_body["data"].get("image", {})

        content_type = image_data.get("contentType", "")

        base64_data = image_data.get("data", "")

        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": system_prompt}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{content_type};base64,{base64_data}"
                        },
                    },
                ],
            },
        ]

    return messages


def format_response(
    request_body: Dict[str, Any], response_text: str, scenario: str
) -> Dict[str, Any]:
    """Format response based on scenario."""
    try:
        response_body: Dict = {
            "recordId": request_body.get("recordId"),
            "warnings": None,
            "errors": [],
            "data": {},
        }

        if scenario == ScenarioType.ENTITY_RECOGNITION.value:
            entities = [
                entity.strip() for entity in response_text.strip("[]").split(",")
            ]
            response_body["data"] = {"result": entities}
        else:

            response_body["data"] = {"result": response_text}

        logger.debug(f"Formatted response: {response_body}")
        return response_body
    except Exception as e:
        logger.error(f"Error formatting response: {e}")
        return {
            "recordId": request_body.get("recordId"),
            "errors": [str(e)],
            "warnings": None,
            "data": None,
        }


def validate_environment() -> tuple[str, str]:
    """Validate required environment variables."""
    api_key = os.getenv("AZURE_OPENAI_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    if not api_key or not endpoint:
        logger.error("Missing required environment variables.")
        raise CustomSkillException("Missing required environment variables", 500)

    logger.info("Environment variables validated successfully.")
    return api_key, endpoint
