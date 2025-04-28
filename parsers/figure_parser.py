import torch
from PIL import Image
import os
import fitz
from transformers import DetrImageProcessor, DetrForObjectDetection

processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def extract_figures(file_path, output_dir="output_figures"):
    os.makedirs(output_dir, exist_ok=True)
    figures_info = []

    doc = fitz.open(file_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        inputs = processor(images=img, return_tensors="pt").to(device)
        outputs = model(**inputs)
        target_sizes = torch.tensor([img.size[::-1]]).to(device)

        results = processor.post_process_object_detection(outputs, threshold=0.8, target_sizes=target_sizes)[0]

        fig_id = 0
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            if score > 0.8:
                x_min, y_min, x_max, y_max = map(int, box.tolist())
                cropped_img = img.crop((x_min, y_min, x_max, y_max))

                image_filename = f"figure_page{page_num+1}_fig{fig_id+1}.png"
                save_path = os.path.join(output_dir, image_filename)
                cropped_img.save(save_path)

                figures_info.append({
                    "page": page_num + 1,
                    "path": save_path,
                    "label": model.config.id2label[label.item()],
                    "score": round(score.item(), 3)
                })

                fig_id += 1

    return figures_info
