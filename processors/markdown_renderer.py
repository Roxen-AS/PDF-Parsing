def render_markdown(output_path, metadata, outlines, links, ocr_text, layout, tables, code_blocks, figures):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Document Metadata\n")
        for k, v in metadata.items():
            f.write(f"- **{k}**: {v}\n")
        
        f.write("\n# Outline\n")
        for item in outlines:
            f.write(f"{'  ' * (item[0]-1)}- {item[1]}\n")

        f.write("\n# Hyperlinks\n")
        for link in links:
            uri = link.get("uri", "N/A")
            f.write(f"- {uri}\n")

        f.write("\n# OCR Text\n")
        for page in ocr_text:
            f.write(f"## Page {page['page_idx'] + 1}\n")
            for block in page['blocks']:
                f.write(f"{block['value']}\n\n")

        f.write("\n# Layout Elements\n")
        for el in layout:
            f.write(f"- {el.type} at {el.block}\n")

        f.write("\n# Tables\n")
        for table in tables:
            for row in table:
                f.write("| " + " | ".join(str(cell) for cell in row) + " |\n")

        f.write("\n# Code Blocks\n")
        for code in code_blocks:
            f.write("```python\n" + code + "\n```\n")

        f.write("\n# Figures\n")
        for fig in figures:
            f.write(f"- Page {fig['page']}: {fig['count']} images detected\n")
