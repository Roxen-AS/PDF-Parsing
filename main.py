#main

import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pdf_to_images import convert_pdf_to_images
from parsers.pymupdf_text_parser import parse_page  
from parsers.table_parser import extract_tables
from parsers.code_block_parser import detect_code_blocks
from parsers.metadata_parser import extract_metadata
from utils.markdown_builder import assemble_markdown
from parsers.figure_parser import extract_figures_with_tf_id

INPUT_PDF = "input/ex2.pdf"
INPUT_IMG_DIR = "input_images"
OUTPUT_MD = "output/rendered.md"
OUTPUT_FIG_DIR = "output_figures"

def run_pipeline():
    
    convert_pdf_to_images(INPUT_PDF, INPUT_IMG_DIR)
    image_files = sorted([os.path.join(INPUT_IMG_DIR, f) for f in os.listdir(INPUT_IMG_DIR) if f.endswith(".png")])
    num_pages = len(image_files)

  
    metadata = extract_metadata(INPUT_PDF)

    
    tables, table_bboxes = extract_tables(INPUT_PDF)

    
    figures, figure_bboxes = extract_figures_with_tf_id(INPUT_PDF, output_dir=OUTPUT_FIG_DIR)

    
    print("🔍 Extracting text with PyMuPDF (skipping figure/table content)...")
    parse_pdf_page = partial(parse_page, pdf_path=INPUT_PDF, figure_bboxes=figure_bboxes, table_bboxes=table_bboxes)
    with ThreadPoolExecutor(max_workers=4) as executor:
        text_blocks = list(executor.map(parse_pdf_page, range(num_pages)))

    
    code_blocks = detect_code_blocks(text_blocks)

    
    markdown = assemble_markdown(text_blocks, [], tables, figures, code_blocks, metadata)

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ Markdown saved to {OUTPUT_MD}")

if __name__ == "__main__":
    run_pipeline()