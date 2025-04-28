import fitz

def extract_metadata(file_path):
    doc = fitz.open(file_path)
    metadata = doc.metadata
    hyperlinks = []

    for page in doc:
        links = page.get_links()
        hyperlinks.extend([l['uri'] for l in links if 'uri' in l])

    return {'metadata': metadata, 'hyperlinks': hyperlinks}
