#main

import os
from concurrent.futures import ThreadPoolExecutor
from pdf_to_images import convert_pdf_to_images
from parsers.hf_ocr_parser import parse_page
from parsers.table_parser import extract_tables
from parsers.code_block_parser import detect_code_blocks
from parsers.metadata_parser import extract_metadata
from utils.markdown_builder import assemble_markdown
from parsers.figure_parser import extract_figures_with_tf_id

INPUT_PDF = "input/example.pdf"
INPUT_IMG_DIR = "input_images"
OUTPUT_MD = "output/rendered.md"
OUTPUT_FIG_DIR = "output_figures"

def run_pipeline():
    convert_pdf_to_images(INPUT_PDF, INPUT_IMG_DIR)
    image_files = sorted([os.path.join(INPUT_IMG_DIR, f) for f in os.listdir(INPUT_IMG_DIR) if f.endswith(".png")])

    with ThreadPoolExecutor(max_workers=4) as executor:
        text_blocks = list(executor.map(parse_page, image_files))

    tables = extract_tables(INPUT_PDF)
    code_blocks = detect_code_blocks(text_blocks)
    metadata = extract_metadata(INPUT_PDF)
    figures = extract_figures_with_tf_id(INPUT_PDF, output_dir=OUTPUT_FIG_DIR)

    markdown = assemble_markdown(text_blocks, [], tables, figures, code_blocks, metadata)

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"✅ Markdown saved to {OUTPUT_MD}")

if __name__ == "__main__":
    run_pipeline()