import sys
from processors.ocr_doctr import extract_text_blocks
from processors.layout_parser import extract_layout
from processors.table_extractor import extract_tables
from processors.code_detector import extract_code_blocks
from processors.figure_detector import detect_figures
from processors.pdf_utils import extract_metadata_and_links, extract_images_from_pdf
from processors.markdown_renderer import render_to_markdown

def main(pdf_path):
    metadata, links = extract_metadata_and_links(pdf_path)
    text_blocks = extract_text_blocks(pdf_path)
    layout = extract_layout(pdf_path)
    tables = extract_tables(pdf_path)
    code_blocks = extract_code_blocks(text_blocks)
    figures = detect_figures(pdf_path)
    images = extract_images_from_pdf(pdf_path)

    markdown_output = render_to_markdown(
        text_blocks, layout, tables, code_blocks, figures, metadata, links, images
    )

    output_path = "output/output.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    print(f"Markdown generated at: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_pdf>")
    else:
        main(sys.argv[1])
