import json
import os
import time
from functools import lru_cache
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from loguru import logger
from openai import AsyncAzureOpenAI

from models import CustomSkillException, ModelConfig, RequestData
from utils import format_response, prepare_messages

app = FastAPI()


@lru_cache(maxsize=1)
def load_custom_prompts() -> Dict[str, str]:
    """Load and cache custom prompts from JSON file."""
    try:
        with open("custom_prompts.json", "r") as file:
            prompts = json.load(file)
            logger.info("Custom prompts loaded successfully.")
            return prompts
    except Exception as e:
        logger.error(f"Failed to load custom prompts: {e}")
        raise CustomSkillException("Failed to load custom prompts", 500)


def validate_environment() -> tuple[str, str]:
    """Validate required environment variables."""
    api_key = os.getenv("AZURE_OPENAI_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    if not api_key or not endpoint:
        logger.error("Missing required environment variables.")
        raise CustomSkillException("Missing required environment variables", 500)

    logger.info("Environment variables validated successfully.")
    return api_key, endpoint


async def call_azure_openai(
    payload: Dict[str, Any], config: ModelConfig
) -> Dict[str, Any]:
    """Make HTTP request to Azure OpenAI using official async client."""

    try:

        client = AsyncAzureOpenAI(
            api_key=config.api_key,
            api_version=config.api_version,
            azure_endpoint=config.endpoint,
            timeout=config.timeout,
            max_retries=config.retry_attempts,
        )

        logger.info(f"Sending request to Azure OpenAI: {payload}")

        response = await client.chat.completions.create(
            model=config.model_deployment,
            messages=payload["messages"],
            temperature=payload.get("temperature", 0.7),
            top_p=payload.get("top_p", None),
            max_tokens=payload.get("max_tokens", 4096),
        )

        logger.info("Successfully received response from Azure OpenAI.")

        return response.model_dump()

    except Exception as e:

        logger.error(f"Error calling Azure OpenAI: {str(e)}")

        raise CustomSkillException(f"Request failed: {str(e)}", 500)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        validate_environment()
        load_custom_prompts()

        return {
            "status": "Healthy",
            "timestamp": time.time(),
            "checks": {"environment": "OK", "prompts": "OK"},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/custom_skill")
async def custom_skill(request: RequestData, scenario: str):
    """Main custom skill endpoint"""
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
        custom_prompts = load_custom_prompts()
        config = ModelConfig()

        response_values = []
        for request_body in input_values:
            try:
                messages = prepare_messages(request_body, scenario, custom_prompts)
                request_payload = {
                    "messages": messages,
                    "temperature": config.temperature,
                    "top_p": config.top_p,
                    "max_tokens": config.max_tokens,
                }

                response_json = await call_azure_openai(
                    payload=request_payload,
                    config=config,
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
