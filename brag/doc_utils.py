import os
from datetime import datetime

BRAG_DOC = "bragdoc.md"

def init_brag_doc():
    if not os.path.exists(BRAG_DOC):
        with open(BRAG_DOC, "w") as f:
            f.write("# Brag Doc\n\n")
        return True
    return False

def add_entry(message: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(BRAG_DOC, "a") as f:
        f.write(f"- [{now}] {message}\n")

def read_history():
    if not os.path.exists(BRAG_DOC):
        return []
    with open(BRAG_DOC, "r") as f:
        return f.readlines()
