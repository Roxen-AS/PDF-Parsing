def render_markdown(text_blocks, tables, code_blocks, figures, metadata, links):
    markdown = ""
    
    # Add metadata
    markdown += f"# {metadata.get('title', 'Document Title')}\n"
    markdown += f"Author: {metadata.get('author', 'Unknown')}\n\n"
    
    # Add text blocks
    markdown += "## Text\n"
    markdown += "\n".join(text_blocks) + "\n\n"
    
    # Add tables
    markdown += "## Tables\n"
    for table in tables:
        for row in table:
            markdown += "| " + " | ".join(row) + " |\n"
        markdown += "\n"
    
    # Add code blocks
    markdown += "## Code\n"
    for code in code_blocks:
        markdown += "```python\n" + code + "\n```\n"
    
    # Add figures
    markdown += "## Figures\n"
    for figure in figures:
        markdown += f"![Figure]({figure})\n"  # Assuming figure is a path or URL
    
    # Add hyperlinks
    markdown += "## Links\n"
    for link in links:
        markdown += f"[{link['uri']}]({link['uri']})\n"
    
    return markdown
