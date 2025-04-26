import re

def detect_code_blocks(text):
    # Heuristic approach to detect code blocks in text
    code_blocks = []
    block = ""
    for line in text.split("\n"):
        if re.match(r'^\s*(def|class|import|from|for|if|else)', line):  # Simple code block heuristic
            block += line + "\n"
        elif block:
            code_blocks.append(block)
            block = ""
    
    return code_blocks
