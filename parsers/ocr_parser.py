ocr_parser
from doctr.models import ocr_predictor
from doctr.io import DocumentFile

model = ocr_predictor(pretrained=True)

def extract_text(file_path):
    doc = DocumentFile.from_pdf(file_path)
    result = model(doc)
    text_blocks = []
    for page in result.pages:
        for block in page.blocks:
            block_text=[]
            for line in block.lines:
                line_text= "".join([word.value for word in line.words])

                block_text.append(line_text)

            text_blocks.append("\n".join(block_text))
    return text_blocks
