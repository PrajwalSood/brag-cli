import os
from datetime import datetime
from typing import List
from pydantic import BaseModel

BRAG_DOC = "bragdoc.md"

class BragEntry(BaseModel):
    timestamp: str
    message: str

def init_brag_doc() -> bool:
    if not os.path.exists(BRAG_DOC):
        with open(BRAG_DOC, "w") as f:
            f.write("# Brag Doc\n\n")
        return True
    return False

def add_entry(message: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = BragEntry(timestamp=now, message=message)
    with open(BRAG_DOC, "a") as f:
        f.write(f"- [{entry.timestamp}] {entry.message}\n")

def read_history() -> List[str]:
    if not os.path.exists(BRAG_DOC):
        return []
    with open(BRAG_DOC, "r") as f:
        return f.readlines()
