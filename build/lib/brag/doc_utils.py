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

def purge_entries_between(start_date: str, end_date: str) -> int:
    """
    Purge brag doc entries between start_date and end_date (inclusive).
    Dates should be in 'YYYY-MM-DD' format.
    Returns the number of entries removed.
    """
    if not os.path.exists(BRAG_DOC):
        return 0
    with open(BRAG_DOC, "r") as f:
        lines = f.readlines()
    header = []
    entries = []
    for line in lines:
        if line.startswith("- ["):
            entries.append(line)
        else:
            header.append(line)
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    kept = []
    removed = 0
    for entry in entries:
        try:
            ts = entry.split(']')[0][3:]
            entry_dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").date()
            if start_dt <= entry_dt <= end_dt:
                removed += 1
                continue
        except Exception:
            pass
        kept.append(entry)
    with open(BRAG_DOC, "w") as f:
        f.writelines(header + kept)
    return removed
