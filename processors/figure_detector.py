import fitz  # PyMuPDF

def detect_figures(pdf_path):
    doc = fitz.open(pdf_path)
    figures = []

    for i in range(len(doc)):
        page = doc[i]
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            figures.append({
                "page": i + 1,
                "type": "figure",
                "ext": ext,
                "data": image_bytes
            })
    return figures
