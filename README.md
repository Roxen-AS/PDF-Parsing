# PDF-Parsing

Pipeline to parse PDF files and convert them into structured Markdown using a combination of models that are time efficient.

PDF --> Images --> DocTR OCR
                     |
                     v
         ┌────────────────────────┐
         │ Element Classifier     │ <-- Rule-based + ML tagging
         └────────────────────────┘
                     |
                     v
         ┌────────────────────────┐
         │ Markdown Converter     │ <-- Render structured .md
         └────────────────────────┘
