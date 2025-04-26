# processors/figure_detector.py

from ultralytics import YOLO
import cv2
import os

# Load the YOLOv8 Nano model (very lightweight)
model = YOLO('yolov8n.pt')

def detect_figures(image_path):
    """
    Detects figures in the given image using YOLOv8.
    
    Args:
        image_path (str): Path to the input image.

    Returns:
        List[Dict]: A list of figure bounding boxes in [x_min, y_min, x_max, y_max] format.
    """
    results = model(image_path)
    
    figures = []
    for box in results[0].boxes.xyxy.cpu().numpy():
        x_min, y_min, x_max, y_max = box.tolist()
        figures.append({
            "bbox": [x_min, y_min, x_max, y_max],
            "label": "figure"  # or custom label if needed
        })
    
    return figures

if __name__ == "__main__":
    # Example usage
    image_path = "path/to/your/image.jpg"
    detections = detect_figures(image_path)
    print(detections)
