#hf_ocr_parser.py

import fitz  

def parse_page(page_path_or_number, pdf_path, figure_bboxes=None, table_bboxes=None):
    """
    Extracts text from a PDF page while ignoring image areas.
    `figure_bboxes` and `table_bboxes` are in PDF coordinate space (not pixels).
    """
    doc = fitz.open(pdf_path)
    
    if isinstance(page_path_or_number, int):
        page = doc.load_page(page_path_or_number)
    else:
        raise ValueError("Use page index (int) when calling parse_page with PyMuPDF.")

    # Optional: mask out bbox regions
    mask_areas = (figure_bboxes or []) + (table_bboxes or [])
    words = page.get_text("words")  
    
    filtered_words = []
    for w in words:
        x0, y0, x1, y1, word = w[:5]
        skip = False
        for bx1, by1, bx2, by2 in mask_areas:
            if not (x1 < bx1 or x0 > bx2 or y1 < by1 or y0 > by2):
                skip = True
                break
        if not skip:
            filtered_words.append((x0, y0, word))

    
    filtered_words.sort(key=lambda x: (round(x[1]), x[0]))  
    lines = []
    current_y = None
    current_line = []

    for x, y, word in filtered_words:
        if current_y is None or abs(current_y - y) > 5:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_y = y
        else:
            current_line.append(word)
    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)