import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pdf_to_images import convert_pdf_to_images
from parsers.table_parser import extract_tables
from parsers.figure_parser import extract_figures_with_tf_id
from parsers.code_block_parser import detect_code_blocks
from parsers.metadata_parser import extract_metadata
from utils.markdown_builder import assemble_markdown
from easyocr import Reader

INPUT_PDF = "input/ex2.pdf"
INPUT_IMG_DIR = "input_images"
OUTPUT_MD = "output/rendered.md"
OUTPUT_FIG_DIR = "output_figures"


ocr_reader = Reader(['en'], gpu=True)  

def run_pipeline():
    
    convert_pdf_to_images(INPUT_PDF, INPUT_IMG_DIR)
    image_files = sorted([os.path.join(INPUT_IMG_DIR, f) for f in os.listdir(INPUT_IMG_DIR) if f.endswith(".png")])
    num_pages = len(image_files)

    metadata = extract_metadata(INPUT_PDF)
    tables, table_bboxes = extract_tables(INPUT_PDF)
    figures, figure_bboxes = extract_figures_with_tf_id(INPUT_PDF, output_dir=OUTPUT_FIG_DIR)

    print("🔍 Performing OCR on each page image...")
    ocr_results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        ocr_results = list(executor.map(perform_ocr, image_files))

    code_blocks = detect_code_blocks(ocr_results)

    markdown = assemble_markdown(ocr_results, [], tables, figures, code_blocks, metadata)

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ Markdown saved to {OUTPUT_MD}")

def perform_ocr(image_file):
    result = ocr_reader.readtext(image_file)
    text = " ".join([item[1] for item in result])  
    return text

if __name__ == "__main__":
    run_pipeline()
