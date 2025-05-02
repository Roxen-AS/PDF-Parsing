#hf_ocr_parser

from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
import json

processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base", use_fast=True)
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base", use_fast=True)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def parse_page(image_path):
    image = Image.open(image_path).convert("RGB")
    task_prompt = "<s> <ocr>"  # or <s> <docvqa> for other tasks

    inputs = processor(images=image, text=task_prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=512)

    generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    return generated_text.strip()

def donut_json_to_markdown(data):
    md = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                md.append(f"## {key.capitalize()}")
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            md.append(f"- **{k}:** {v}")
                    else:
                        md.append(f"- {item}")
            elif isinstance(value, dict):
                md.append(f"## {key.capitalize()}")
                for k, v in value.items():
                    md.append(f"- **{k}:** {v}")
            else:
                md.append(f"### {key}: {value}")
    return "\n".join(md)
