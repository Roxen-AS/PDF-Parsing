import re

def extract_code_blocks(text_blocks):
    code_blocks = []
    code_pattern = re.compile(r"(?:\s{4}|\t).+")
    for block in text_blocks:
        if code_pattern.search(block):
            code_blocks.append(block)
    return code_blocks
