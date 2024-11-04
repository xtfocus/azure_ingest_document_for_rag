import base64
import json
from io import BytesIO
from typing import Any, Dict, Optional

from PIL import Image


def json_file_load(file_path: str) -> Dict[str, Any]:
    """
    Load JSON file as a Python dictionary.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
        return data


def get_image_format(base64_source: str) -> Optional[str]:
    """
    Retrieve the format of an image from a base64-encoded string.

    Args:
        base64_source (str): The base64-encoded image data.

    Returns:
        Optional[str]: The format of the image (e.g., 'JPEG', 'PNG') or None if format can't be determined.
    """
    image_stream = BytesIO(base64.b64decode(base64_source))
    image = Image.open(image_stream)
    return image.format
