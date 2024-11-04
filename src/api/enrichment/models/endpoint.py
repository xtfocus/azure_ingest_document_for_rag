"""
File: endpoint.py
"""

from typing import Literal, Optional

from pydantic import BaseModel, conlist, constr


class Cache(BaseModel):
    """
    Configuration for caching in media enrichment requests.

    Attributes:
        enabled (bool): Indicates if caching is enabled for the request.
        key_format (Optional[str]): The format string for generating cache keys,
            with "{hash}" as a placeholder for the generated hash of the request data.
            Default is "{hash}".
        expiry (Optional[str]): The duration for which the cached item remains
            valid, in the format "dd:hh:mm:ss" (days, hours, minutes, seconds).
            Example: "01:12:30:00" for 1 day, 12 hours, and 30 minutes.
    """

    enabled: bool
    key_format: Optional[str] = "{hash}"
    expiry: Optional[constr(pattern=r"^\d{2}:\d{2}:\d{2}:\d{2}$")] = None


class Classifier(BaseModel):
    enabled: bool
    threshold: Optional[float] = 0.8


class Mllm(BaseModel):
    enabled: Optional[bool]
    prompt: str
    llm_kwargs: Optional[dict] = {}
    model: str
    detail_mode: Optional[Literal["low", "high", "auto"]] = "auto"


class Features(BaseModel):
    cache: Cache
    classifier: Classifier
    mllm: Mllm


class MediaEnrichmentRequest(BaseModel):
    images: conlist(str, min_length=0, max_length=10)  # Base64-encoded images
    features: Features


class GeneratedResponse(BaseModel):
    content: str


class MediaEnrichmentResponse(BaseModel):
    generated_response: Optional[GeneratedResponse]
    classifier_result: Optional[str]
