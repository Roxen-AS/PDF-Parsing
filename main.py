import sys
from processors.ocr_doctr import extract_text_blocks
from processors.layout_parser import detect_layout
from processors.table_extractor import extract_tables
from processors.code_detector import detect_code_blocks
from processors.figure_detector import detect_figures
from processors.pdf_utils import extract_metadata_and_links
from processors.markdown_renderer import render_markdown
from PIL import Image
import fitz

pdf_path = sys.argv[1]
output_path = "output/rendered.md"


metadata, outlines, links = extract_metadata_and_links(pdf_path)


ocr_text = extract_text_blocks(pdf_path)


doc = fitz.open(pdf_path)
layout_blocks = []
for page in doc:
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    layout = detect_layout(image)
    layout_blocks.extend(layout)


tables = extract_tables(pdf_path)


code_blocks = detect_code_blocks(ocr_text)


figures = detect_figures(pdf_path)


render_markdown(output_path, metadata, outlines, links, ocr_text, layout_blocks, tables, code_blocks, figures)
