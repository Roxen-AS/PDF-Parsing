from doctr.io import DocumentFile  # Changed import path
from doctr.models import ocr_predictor
from tqdm import tqdm
import torch

def extract_text_blocks(pdf_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load document with explicit device allocation
    doc = DocumentFile.from_pdf(pdf_path).as_images(device=device)
    
    # Initialize model with proper config
    model = ocr_predictor(
        det_arch='db_resnet50', 
        reco_arch='crnn_vgg16_bn',
        pretrained=True
    ).to(device)
    
    # Process in batches
    result = model(doc)
    
    extracted_text = []
    for page in tqdm(result.pages, desc="Processing pages"):
        page_text = []
        for block in page.blocks:
            block_text = " ".join([line.value for line in block.lines])
            page_text.append(block_text)
        extracted_text.append("\n\n".join(page_text))
    
    return "\f".join(extracted_text)  # Form feed as page separator
