#hf_ocr_parser.py

from PIL import Image, ImageDraw
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# Load doctr OCR model once
model = ocr_predictor(pretrained=True)

def mask_bboxes(image, bboxes):
    draw = ImageDraw.Draw(image)
    for box in bboxes:
        draw.rectangle(box, fill="white")
    return image

def extract_text_from_doctr_result(result):
    """
    Extract and sort lines top-to-bottom from Doctr's output.
    Returns one unified string per page.
    """
    pages_text = []

    for page in result.pages:
        lines = []

        for block in page.blocks:
            for line in block.lines:
                text_line = " ".join([word.value for word in line.words]).strip()
                if text_line:
                    lines.append((line.geometry[0][1], text_line))  # (y position, text)

        # Sort lines vertically and join
        lines.sort(key=lambda x: x[0])
        page_text = "\n".join([t[1] for t in lines])
        pages_text.append(page_text)

    return pages_text

def parse_page(image_path, figure_bboxes=None, table_bboxes=None):
    """
    Uses Doctr OCR + layout ordering to extract text from an image,
    masking figures/tables before processing.
    """
    image = Image.open(image_path).convert("RGB")

    all_bboxes = (figure_bboxes or []) + (table_bboxes or [])
    if all_bboxes:
        image = mask_bboxes(image, all_bboxes)

    # Run Doctr
    doc = DocumentFile.from_images(image)
    result = model(doc)

    # Convert Doctr result to clean, readable text
    page_texts = extract_text_from_doctr_result(result)
    return "\n".join(page_texts).strip()
