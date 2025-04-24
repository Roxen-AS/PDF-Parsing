from doctr.io import DocumentFile
from doctr.models import ocr_predictor

def extract_text_blocks(pdf_path):
    doc = DocumentFile.from_pdf(pdf_path)
    model = ocr_predictor(pretrained=True)
    result = model(doc)

    blocks = []
    for page in result.pages:
        for block in page.blocks:
            text = " ".join([line.value for line in block.lines])
            blocks.append(text)
    return blocks
