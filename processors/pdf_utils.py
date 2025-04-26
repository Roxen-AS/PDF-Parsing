import fitz  

def extract_metadata_and_links(pdf_path):
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    outlines = doc.get_toc()
    links = []

    for page in doc:
        links.extend(page.get_links())

    return metadata, outlines, links

def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        img_list = page.get_images(full=True)
        for img_index, img in enumerate(img_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            images.append((page_num, image_bytes, image_ext))

    return images
