import fitz  # PyMuPDF

def extract_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    metadata = doc.metadata  # Returns metadata like title, author, etc.
    return metadata

def extract_links(pdf_path):
    doc = fitz.open(pdf_path)
    links = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for link in page.get_links():
            links.append(link)
    return links
