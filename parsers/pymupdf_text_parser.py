#pymupdf_text_parser.py

#Alternate and slower technique for text extraction using PyMuPDF

import fitz  

def parse_page(page_index, pdf_path, figure_bboxes=None, table_bboxes=None):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_index)
    all_bboxes = (figure_bboxes or []) + (table_bboxes or [])

    
    words = page.get_text("words")

    filtered_words = []
    for w in words:
        x0, y0, x1, y1, word = w[:5]
        skip = False
        for bx1, by1, bx2, by2 in all_bboxes:
            if not (x1 < bx1 or x0 > bx2 or y1 < by1 or y0 > by2):
                skip = True
                break
        if not skip:
            filtered_words.append((x0, y0, word))

    
    filtered_words.sort(key=lambda x: (round(x[1]), x[0]))

  
    lines = []
    current_line = []
    current_y = None

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