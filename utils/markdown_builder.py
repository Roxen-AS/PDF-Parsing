#markdown_builder

def assemble_markdown(text_blocks, layout_blocks, tables, figures, code_blocks, metadata):
    md = []

    md.append(f"# Document Metadata\n\n")
    for key, value in metadata['metadata'].items():
        md.append(f"**{key}:** {value}\n")

    if metadata['hyperlinks']:
        md.append("\n# Hyperlinks\n")
        for link in metadata['hyperlinks']:
            md.append(f"- {link}\n")

    md.append("\n# Content\n")
    for block in text_blocks:
        if block in code_blocks:
            md.append(f"\n```python\n{block}\n```\n")
        else:
            md.append(f"\n{block}\n")

    if tables:
        md.append("\n# Tables\n")
        for table in tables:
            for row in table:
                md.append("| " + " | ".join(cell or "" for cell in row) + " |")
            md.append("\n")

    if figures:
        md.append("\n# Figures\n")
        for fig in figures:
            confidence = fig.get('score', 'N/A')
            md.append(f"\n![Figure page {fig['page']}]({fig['path']})\n_Label: {fig['label']} | Confidence: {confidence}_\n")

    return "\n".join(md)