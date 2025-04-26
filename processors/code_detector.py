import re

def detect_code_blocks(text_blocks):
    code_blocks = []
    non_code_blocks = []

    code_pattern = re.compile(r'(^\s{4,}|\n\s{4,})', re.MULTILINE)

    for block in text_blocks:
        if code_pattern.search(block['text']):
            code_blocks.append(block)
        else:
            non_code_blocks.append(block)

    return code_blocks, non_code_blocks
