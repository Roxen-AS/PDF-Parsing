import os
import fitz  # PyMuPDF
from PIL import Image

def convert_pdf_to_images(pdf_path, output_folder="input_images"):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(output_folder, f"page{i+1}.png")
        Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(img_path)
