import layoutparser as lp

def detect_layout(image):
    model = lp.EfficientDetLayoutModel(
        config_path='lp://PubLayNet/efficientdet/M',
        label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
        extra_config=["CACHE_DIR=./cache"]
    )
    layout = model.detect(image)
    return layout
