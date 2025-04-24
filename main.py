import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'processors')))

from pdf_utils import extract_metadata_and_links, extract_images_from_pdf
from ocr_doctr import extract_text_blocks
from layout_parser import detect_layout_blocks
from table_extractor import extract_tables
from code_detector import detect_code_blocks
from figure_detector import detect_figures
from markdown_renderer import render_markdown

import fitz  # PyMuPDF
import time

def main(pdf_path):
    start_time = time.time()

    doc = fitz.open(pdf_path)
    metadata, links = extract_metadata_and_links(doc)
    images = extract_images_from_pdf(doc)

    all_text_blocks, all_layout_blocks = [], []
    all_tables, all_figures, all_code_blocks = [], [], []

    for page_num, page in enumerate(doc):
        image = page.get_pixmap(dpi=300).pil_tobytes("jpeg")

        text_blocks = extract_text_blocks(image)
        layout_blocks = detect_layout_blocks(image)
        tables = extract_tables(page)
        code_blocks = detect_code_blocks(text_blocks)
        figures = detect_figures(image)

        all_text_blocks.extend(text_blocks)
        all_layout_blocks.extend(layout_blocks)
        all_tables.extend(tables)
        all_code_blocks.extend(code_blocks)
        all_figures.extend(figures)

    markdown = render_markdown(
        metadata, all_text_blocks, all_layout_blocks, all_tables,
        all_code_blocks, all_figures, links
    )

    os.makedirs("output", exist_ok=True)
    output_filename = os.path.splitext(os.path.basename(pdf_path))[0] + "_output.md"
    output_path = os.path.join("output", output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✓ PDF converted to Markdown in {time.time() - start_time:.2f}s → {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py input/<your_pdf_file>")
    else:
        main(sys.argv[1])
