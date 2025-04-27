from doctr.io import DocumentFile
from doctr.models import ocr_predictor

import numpy as np

# Load OCR model once
ocr_model = ocr_predictor(pretrained=True)

def extract_text_blocks(image):
    """
    Extract text blocks from a PIL Image using DocTR OCR.
    """
    # Convert PIL Image to NumPy array (DocTR expects NumPy)
    img_array = np.array(image)

    doc = DocumentFile.from_images([img_array])
    result = ocr_model(doc)

    text_blocks = []
    for page in result.pages:
        for block in page.blocks:
            text_blocks.append(block.text)
    return text_blocks
