import os
from parsers.ocr_parser import extract_text
#from parsers.layout_parser import extract_layout
from parsers.table_parser import extract_tables
from parsers.figure_parser import extract_figures
from parsers.code_block_parser import detect_code_blocks
from parsers.metadata_parser import extract_metadata
from utils.markdown_builder import assemble_markdown

INPUT_DIR = "input"
OUTPUT_DIR = "output"
INPUT_FILE = os.path.join(INPUT_DIR, "bp.pdf")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "rendered.md")

def process_pdf(file_path, output_path):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    text_blocks = extract_text(file_path)
    #layout_blocks = extract_layout(file_path)
    tables = extract_tables(file_path)
    figures = extract_figures(file_path)
    code_blocks = detect_code_blocks(text_blocks)
    metadata = extract_metadata(file_path)

    markdown = assemble_markdown(
        text_blocks, 
        #layout_blocks, 
        tables, figures, code_blocks, metadata
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"✅ Markdown saved to: {output_path}")

if __name__ == "__main__":
    process_pdf(INPUT_FILE, OUTPUT_FILE)
