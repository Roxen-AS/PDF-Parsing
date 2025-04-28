#table_parser
import pdfplumber

def extract_tables(file_path):
    tables = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables.extend(page.extract_tables())
    return tables
