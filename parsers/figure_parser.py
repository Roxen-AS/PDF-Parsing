#figure_parser

from pdf2image import convert_from_path
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
import os
import gc
import torch

def pdf_to_image(pdf_path, dpi=150):
    return convert_from_path(pdf_path, dpi=dpi)

def tf_id_detection(image, model, processor):
    prompt = "<OD>"
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=1024,
        do_sample=False,
        num_beams=3
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    annotation = processor.post_process_generation(generated_text, task="<OD>", image_size=(image.width, image.height))
    return annotation["<OD>"]

def save_image_from_bbox(image, annotation, page_num, output_dir):
    figures = []
    bboxes = []

    for i, bbox in enumerate(annotation['bboxes']):
        label = annotation['labels'][i]
        x1, y1, x2, y2 = bbox
        cropped_image = image.crop((x1, y1, x2, y2))
        fig_path = os.path.join(output_dir, f"figure_page{page_num+1}_{label}_{i+1}.png")
        cropped_image.save(fig_path)

        figures.append({
            "page": page_num + 1,
            "label": label,
            "box": [x1, y1, x2, y2],
            "path": fig_path
        })
        bboxes.append([x1, y1, x2, y2])

    return figures, bboxes

def extract_figures_with_tf_id(pdf_path, output_dir="output_figures"):
    os.makedirs(output_dir, exist_ok=True)
    model_id = "yifeihu/TF-ID-large"

    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

    images = pdf_to_image(pdf_path)
    all_figures = []
    all_bboxes = []

    for page_num, image in enumerate(images):
        print(f"Detecting figures on page {page_num+1}...")

        try:
            annotation = tf_id_detection(image, model, processor)
            figures, bboxes = save_image_from_bbox(image, annotation, page_num, output_dir)
            all_figures.extend(figures)
            all_bboxes.extend(bboxes)
        except Exception as e:
            print(f"Error processing page {page_num+1}:", e)

        gc.collect()
        torch.cuda.empty_cache()

    return all_figures, all_bboxes
