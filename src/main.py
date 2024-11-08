import os
import time
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from loguru import logger

from .custom_prompts import custom_prompts
from .globals import clients, configs
from .models import CustomSkillException, RequestData
from .requests_utils import format_response, prepare_messages

router = APIRouter()


def validate_environment() -> tuple[str, str]:
    """Validate required environment variables."""

    api_key = os.getenv("AZURE_OPENAI_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    if not api_key or not endpoint:
        logger.error("Missing required environment variables.")
        raise CustomSkillException("Missing required environment variables", 500)

    logger.info("Environment variables validated successfully.")
    return api_key, endpoint


async def call_azure_openai(client, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Make HTTP request to Azure OpenAI using official async client."""

    try:
        response = await client.chat.completions.create(**payload)

        return response.model_dump()

    except Exception as e:

        logger.error(f"Error calling Azure OpenAI: {str(e)}")

        raise CustomSkillException(f"Request failed: {str(e)}", 500)


@router.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        validate_environment()
        return {
            "status": "Healthy",
            "timestamp": time.time(),
            "checks": {"environment": "OK"},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/custom_skill")
async def custom_skill(request: RequestData, scenario: str):
    """Main custom skill endpoint"""

    oaiclient = clients["chat-completion-model"]
    oaiconfig = configs["chat-completion-model"]

    try:
        # Validate scenario
        if not scenario:
            raise HTTPException(status_code=400, detail="Missing scenario in headers")

        input_values = request.values
        if not input_values:
            raise HTTPException(
                status_code=400, detail="Missing values in request body"
            )

        # Initialize configurations
        validate_environment()
        logger.info(f"{oaiconfig}")

        response_values = []
        for request_body in input_values:
            try:
                messages = prepare_messages(request_body, scenario, custom_prompts)
                request_payload = {
                    "messages": messages,
                    "temperature": oaiconfig.temperature,
                    "top_p": oaiconfig.top_p,
                    "max_tokens": oaiconfig.max_tokens,
                    "model": oaiconfig.MODEL_DEPLOYMENT,
                }

                response_json = await call_azure_openai(
                    oaiclient,
                    payload=request_payload,
                )

                response_text = response_json["choices"][0]["message"]["content"]
                response_values.append(
                    format_response(request_body, response_text, scenario)
                )

            except Exception as e:
                response_values.append(
                    {
                        "recordId": request_body.get("recordId"),
                        "errors": [str(e)],
                        "warnings": None,
                        "data": None,
                    }
                )

        return {"values": response_values}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
