#code_block_parser

def detect_code_blocks(text_blocks):
    code_blocks = []
    for block in text_blocks:
        if '```' in block or (block.count('\n') > 5 and '{' in block and '}' in block):
            code_blocks.append(block)
    return code_blocks
