#table_parser

import pdfplumber

def extract_tables(pdf_path):
    tables = []
    table_bboxes = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            try:
                extracted_tables = page.extract_tables()

                for table in extracted_tables:
                    if not table:
                        continue

                    tables.append(table)

                    try:
                        bbox = page.bbox  
                    except Exception:
                        bbox = [0, 0, page.width, page.height]

                    table_bboxes.append([bbox[0], bbox[1], bbox[2], bbox[3]])

            except Exception as e:
                print(f"[WARN] Failed to extract table on page {page_number}: {e}")

    return tables, table_bboxes