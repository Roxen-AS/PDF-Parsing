# PDF-Parsing

Pipeline to parse PDF files and convert them into structured Markdown using a combination of models that are time efficient.


![alt text](image.png)


This project is a high-performance pipeline that converts PDF documents into clean, structured Markdown using multiple specialized models. It supports extraction of:

Text blocks (via DocTR OCR)

Document layout structure (via LayoutParser)

Tables (via pdfplumber)

Code blocks (via heuristics)

Figures (via Detectron2)

Hyperlinks & metadata (via PyMuPDF)

It’s designed for accuracy, modularity, and speed, making it ideal for large-scale document parsing or archiving workflows.