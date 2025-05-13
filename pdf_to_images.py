#pdf_to_images.py

from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, output_dir="input_images"):
    """
    Converts PDF pages to images and saves them in the specified output directory.
    Args:
        pdf_path (str): Path to the input PDF file.
        output_dir (str): Directory to save the images. Default is "input_images".
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert PDF to images
    images = convert_from_path(pdf_path)

    # Save images
    for i, img in enumerate(images):
        img.save(os.path.join(output_dir, f"page_{i + 1}.png"), "PNG")

    print(f"✅ {len(images)} pages converted to images and saved to {output_dir}")
