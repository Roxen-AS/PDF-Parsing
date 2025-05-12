import logging
from pathlib import Path
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from cleantext import clean
import re
import time
from spellchecker import SpellChecker
from easyocr import Reader  

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S",
)

spell = SpellChecker()

def convert_image_to_text(image_path, ocr_model=None):

    
    ocr_reader = Reader(['en'], gpu=True)  

    
    img = DocumentFile.from_images([image_path])  
    result = ocr_model(img)
    
    raw_text = result2text(result)
    processed_text = [format_ocr_out(r) for r in raw_text]
    final_text = [postprocess(t) for t in processed_text]

    return "\n".join(final_text)

def result2text(result, as_text=False) -> str or list:
    """Convert OCR result to text"""

    full_doc = []
    for i, page in enumerate(result.pages, start=1):
        text = ""
        for block in page.blocks:
            text += "\n\t"
            for line in block.lines:
                for word in line.words:
                    text += word.value + " "
        full_doc.append(text)

    return "\n".join(full_doc) if as_text else full_doc

def postprocess(text: str) -> str:
    """Post-processes text after OCR"""
    proc = corr(cleantxt_ocr(text))

    for k, v in custom_replace_list.items():
        proc = proc.replace(str(k), str(v))

    proc = corr(proc)

    for k, v in replace_corr_exceptions.items():
        proc = proc.replace(str(k), str(v))

    return eval_and_replace(proc)

