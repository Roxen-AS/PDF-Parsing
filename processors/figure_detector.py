import fitz  

def detect_figures(pdf_path):
    doc = fitz.open(pdf_path)
    figures = []

    for i, page in enumerate(doc):
        img_list = page.get_images(full=True)
        if img_list:
            figures.append({
                "page": i + 1,
                "count": len(img_list),
                "image_ids": [img[0] for img in img_list],
            })

    return figures
