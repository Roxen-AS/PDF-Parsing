import layoutparser as lp
from torchvision.models.detection import efficientdet_b0

model = lp.EfficientDetLayoutModel('lp://PubLayNetEfficientDet/lite')

def extract_layout(file_path):
    layouts = []
    pdf = lp.io.load_pdf(file_path)
    for page in pdf:
        layout = model.detect(page)
        layouts.append(layout)
    return layouts
