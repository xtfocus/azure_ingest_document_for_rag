import base64
import io
from typing import List

import fitz  # PyMuPDF


def page_contains_text(page: fitz.Page) -> bool:
    """
    Checks if a PyMuPDF page contains any non-empty text.

    Args:
        page (fitz.Page): A single page of a PyMuPDF document.

    Returns:
        bool: True if the page contains non-empty text, False otherwise.
    """
    text = page.get_text()
    return bool(text.strip())  # Check if there's any non-empty text


def doc_contains_text(doc: fitz.Document) -> bool:
    """
    Checks if any page in a PyMuPDF document contains non-empty text.

    Args:
        doc (fitz.Document): A PyMuPDF document object.

    Returns:
        bool: True if any page in the document contains non-empty text, False otherwise.
    """
    for page in doc:
        if page_contains_text(page):
            return True
    return False


def pdf_blob_to_pymupdf_doc(blob: bytes) -> fitz.Document:
    """
    Converts a PDF byte blob into a PyMuPDF Document object.

    Args:
        blob (bytes): A byte blob representing a PDF file.

    Returns:
        fitz.Document: The PyMuPDF Document object created from the byte blob.
    """
    return fitz.open(filetype="pdf", stream=blob)


def extract_single_image(doc: fitz.Document, xref: int) -> fitz.Pixmap:
    """
    Extracts a single image from the document given its xref.
    Converts it to RGB format if necessary and returns the Pixmap.

    Args:
        doc (fitz.Document): The PyMuPDF document object containing the image.
        xref (int): The xref number of the image to extract.

    Returns:
        fitz.Pixmap: A Pixmap object of the extracted image.
    """
    base_image = doc.extract_image(
        xref
    )  # Extract image base data if needed for other purposes
    pix = fitz.Pixmap(doc, xref)  # Create the Pixmap for the image
    if pix.n > 3:  # Convert to RGB if necessary
        pix = fitz.Pixmap(fitz.csRGB, pix)
    return pix


def page_extract_images(page: fitz.Page) -> List[fitz.Pixmap]:
    """
    Extracts all images on a given page as Pixmap objects.

    Args:
        page (fitz.Page): A single page of a PyMuPDF document.

    Returns:
        List[fitz.Pixmap]: A list of Pixmap objects for each image on the page.
    """
    images = []
    doc: fitz.Document = page.parent

    for img_index, img in enumerate(page.get_images()):
        xref = img[0]
        pix = extract_single_image(doc, xref)
        images.append(pix)
    return images


def get_images_as_base64(page: fitz.Page) -> List[str]:
    """
    Converts all images on a given page to base64-encoded strings.

    Args:
        page (fitz.Page): A single page of a PyMuPDF document.

    Returns:
        List[str]: A list of base64-encoded strings, each representing an image on the page.
    """
    images_base64 = []
    images = page_extract_images(page)  # Get all images on the page

    for pix in images:
        # Convert Pixmap to PNG format in-memory
        img_buffer = io.BytesIO(pix.tobytes("png"))
        # Encode PNG binary data as base64 string
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
        images_base64.append(img_base64)

    return images_base64
