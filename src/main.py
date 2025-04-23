import os
from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import fitz  # PyMuPDF

INPUT_PDF = "input/example.pdf"
OUTPUT_MD = "output/example.md"

def convert_pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    image_list = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img_path = f"page_{i}.png"
        pix.save(img_path)
        image_list.append(img_path)
    return image_list

def classify_text(text):
    """Naive classification for demo: Detect titles, headers, etc."""
    text = text.strip()
    if not text:
        return ""
    if text.isupper() and len(text.split()) <= 6:
        return f"# {text}"
    if text.endswith(":") and len(text.split()) <= 10:
        return f"## {text}"
    return text

def convert_to_markdown(blocks):
    md = ""
    for block in blocks:
        for line in block:
            content = line.value
            formatted = classify_text(content)
            if formatted:
                md += formatted + "\n\n"
    return md

def main():
    print("[INFO] Converting PDF pages to images...")
    images = convert_pdf_to_images(INPUT_PDF)

    print("[INFO] Running DocTR OCR...")
    model = ocr_predictor(pretrained=True, det_arch='db_resnet50', reco_arch='crnn_mobilenet_v3_small')
    doc = DocumentFile.from_images(images)
    result = model(doc)

    print("[INFO] Converting OCR output to Markdown...")
    md_content = convert_to_markdown(result.pages)

    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[DONE] Markdown saved to: {OUTPUT_MD}")

    # Cleanup temporary image files
    for img in images:
        os.remove(img)

if __name__ == "__main__":
    main()
