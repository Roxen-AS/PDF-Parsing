import os
from processors.ocr_doctr import extract_text_blocks
from processors.layout_parser import detect_layout
from processors.table_extractor import extract_tables
from processors.code_detector import detect_code_blocks
from processors.figure_detector import detect_figures
from processors.pdf_utils import extract_hyperlinks_and_metadata
from processors.markdown_renderer import render_markdown

import fitz  # PyMuPDF
import io
from PIL import Image

INPUT_PDF = "input/example.pdf"
OUTPUT_MD = "output/rendered.md"

def pdf_to_images_in_memory(pdf_path):
    """
    Converts each page of the PDF into in-memory PIL Images (no disk writes).
    """
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        images.append(image)
    return images

def main():
    # Step 1: Convert PDF pages to in-memory images
    images = pdf_to_images_in_memory(INPUT_PDF)

    all_content = []

    for img in images:  # img is now a PIL Image
        # Step 2: Extract text blocks
        text_blocks = extract_text_blocks(img)

        # Step 3: Detect document layout
        layout = detect_layout(img)

        # Step 4: Extract tables
        tables = extract_tables(INPUT_PDF)

        # Step 5: Detect code blocks
        code_blocks = detect_code_blocks(text_blocks)

        # Step 6: Detect figures
        figures = detect_figures(img)

        page_content = {
            "text_blocks": text_blocks,
            "layout": layout,
            "tables": tables,
            "code_blocks": code_blocks,
            "figures": figures
        }
        all_content.append(page_content)

    # Step 7: Extract hyperlinks and metadata
    hyperlinks, metadata = extract_hyperlinks_and_metadata(INPUT_PDF)

    # Step 8: Render final Markdown
    render_markdown(all_content, hyperlinks, metadata, OUTPUT_MD)

    print(f"✅ Markdown document generated at {OUTPUT_MD}")

if __name__ == "__main__":
    main()
