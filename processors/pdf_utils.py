import fitz

def extract_metadata_and_links(pdf_path):
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    links = []
    for page in doc:
        links += page.get_links()
    return metadata, links

def extract_images_from_pdf(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            images.append({
                "page": i + 1,
                "ext": base_image["ext"],
                "bytes": base_image["image"]
            })
    return images
