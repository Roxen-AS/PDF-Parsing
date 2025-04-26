from doctr.io import DocumentFile
from doctr.models import ocr_predictor

model = ocr_predictor(pretrained=True)

def extract_text_blocks(pdf_path):
    doc = DocumentFile.from_pdf(pdf_path)
    result = model(doc)
    blocks = result.export()["pages"]
    return blocks
