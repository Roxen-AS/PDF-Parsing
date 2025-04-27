import sys
import os
import tensorflow as tf
import numpy as np
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), 'EfficientDet'))

from efficientdet.efficientdet import efficientdet_keras
from utils import preprocess_image

model = efficientdet_keras(phi=0, num_classes=1, score_threshold=0.5)
model.load_weights('processors/EfficientDet/efficientdet-d0.h5')

def detect_layout(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to read image at {image_path}")
        
    input_image, scale = preprocess_image(image, image_size=512)
    input_image = np.expand_dims(input_image, axis=0)

    boxes, scores, labels = model.predict(input_image)

    boxes /= scale

    detections = []
    for box, score, label in zip(boxes[0], scores[0], labels[0]):
        if score < 0.5:
            continue
        x1, y1, x2, y2 = box
        detections.append({
            "label": int(label),
            "score": float(score),
            "box": [float(x1), float(y1), float(x2), float(y2)],
        })

    return detections
