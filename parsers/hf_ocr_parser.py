#hf_ocr_parser

from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
import json

processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base", use_fast=True)
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def parse_page(image_path):
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)
    task_prompt = "<s>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(pixel_values, decoder_input_ids=decoder_input_ids, max_length=1024)
    raw_output = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    try:
        data = json.loads(raw_output)
        return donut_json_to_markdown(data)
    except json.JSONDecodeError:
        return raw_output

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
