# processors/layout_parser.py

import layoutparser as lp

# Use a light TensorFlow-based EfficientDet model
model = lp.EfficientDetLayoutModel(
    "lp://PubLayNet/efficientdet-lite2/config",  # Or lite0 for even lighter
    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5]
)

def detect_layout(image_path):
    """
    Detects layout elements (text, title, figure, table, etc.) in the document image.

    Args:
        image_path (str): Path to the input image.

    Returns:
        List: Detected layout elements
    """
    layout = model.detect(image_path)
    return layout

if __name__ == "__main__":
    image_path = "path/to/your/image.jpg"
    layout = detect_layout(image_path)
    layout.show()  # visualize
