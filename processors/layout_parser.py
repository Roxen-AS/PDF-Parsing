import layoutparser as lp

def extract_layout(pdf_path):
    model = lp.Detectron2LayoutModel(
        config_path="lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config",
        label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5]
    )
    layout_per_page = model.detect(pdf_path)
    return layout_per_page
