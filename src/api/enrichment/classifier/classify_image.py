"""
File: classify_image.py

Function to categorize images based on tags
"""

from enrichment.config.enrichment_config import enrichment_config
from enrichment.utils.enums import Category


def categorize_image(tags_with_confidence, confidence_score_value):
    """

    The categorize_image function determines whether an image should be processed or ignored based on:

        - Image tags and their confidence scores
        - Predefined ignore rules from classifier_config.json

    Return IGNORE category if:
        - No tags meet confidence threshold
        - "text" tag is missing
        - Tags match any ignore rule group

    The function helps optimize processing by filtering out irrelevant images before they reach more computationally expensive stages of the pipeline.
    """

    # Get ignore rules from config
    categories_tags_values = enrichment_config.classifier_config_data
    categories = categories_tags_values["categories"]
    ignore_tags = set(tuple(tag) for tag in categories["ignore_tags"])

    # limiting tags considered based on confidence score
    tags = [
        tag.name.lower()
        for tag in tags_with_confidence
        if tag.confidence >= confidence_score_value
    ]

    # when there is no text then ignore
    if not tags or not any(tag in tags for tag in ["text"]):
        return Category.IGNORE
    # tags that can be ignored
    elif any(all(tag in tags for tag in subset) for subset in ignore_tags):
        return Category.IGNORE
    # fallback for everything else
    else:
        return Category.GPT_VISION
