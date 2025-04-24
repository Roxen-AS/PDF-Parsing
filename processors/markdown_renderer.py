def render_to_markdown(text_blocks, layout, tables, code_blocks, figures, metadata, links, images):
    md = []

    md.append(f"# Document Metadata\n\n{metadata}\n")
    md.append(f"# Hyperlinks\n\n{links}\n")
    
    md.append("## Text Blocks\n")
    for block in text_blocks:
        md.append(block + "\n")

    md.append("## Tables\n")
    for table in tables:
        for row in table:
            md.append("| " + " | ".join(row) + " |")
        md.append("")

    md.append("## Code Blocks\n")
    for code in code_blocks:
        md.append("```python\n" + code + "\n```")

    md.append("## Figures\n")
    for fig in figures:
        md.append(f"Figure on page {fig['page']}, type: {fig['ext']}")

    md.append("## Images\n")
    for img in images:
        md.append(f"Image on page {img['page']}, format: {img['ext']}")

    return "\n".join(md)
