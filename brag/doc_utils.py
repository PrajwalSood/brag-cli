import os
import platform
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from brag.constants import (
    BRAG_DOC_FILENAME, TIMESTAMP_FORMAT, DATE_FORMAT, BRAG_DOC_HEADER,
    WINDOWS_BASE_PATH, DARWIN_APP_SUPPORT_PATH, LINUX_DATA_PATH, XDG_DATA_HOME_ENV,
    CATEGORY_FORMAT, GIT_INIT_COMMIT_MESSAGE, IS_TESTING, TEST_DIR
)

# Determine brag doc path based on OS

def get_brag_doc_path(test_path: str = None) -> str:
    """
    Get the path to the brag document file.
    
    Args:
        test_path: Optional path for testing purposes. If None, normal path resolution is used.
        
    Returns:
        Path to the brag document file.
    """
    # Use explicit test path if provided
    if test_path:
        return test_path
        
    # Import constants dynamically to get current values
    from brag import constants
    
    # Use test directory if in testing mode
    if constants.IS_TESTING:
        return os.path.join(constants.TEST_DIR, BRAG_DOC_FILENAME)
        
    # Normal path resolution based on OS
    home = os.path.expanduser("~")
    if platform.system() == "Windows":
        base = os.environ.get(WINDOWS_BASE_PATH, home)
        return os.path.join(base, BRAG_DOC_FILENAME)
    elif platform.system() == "Darwin":
        return os.path.join(home, DARWIN_APP_SUPPORT_PATH, BRAG_DOC_FILENAME)
    else:  # Linux and others
        xdg = os.environ.get(XDG_DATA_HOME_ENV, os.path.join(home, LINUX_DATA_PATH))
        return os.path.join(xdg, BRAG_DOC_FILENAME)

class BragEntry(BaseModel):
    timestamp: str
    message: str
    category: Optional[str] = None

def init_brag_doc() -> bool:
    brag_doc = get_brag_doc_path()
    if not os.path.exists(brag_doc):
        os.makedirs(os.path.dirname(brag_doc), exist_ok=True)
        with open(brag_doc, "w") as f:
            f.write(BRAG_DOC_HEADER)
        return True
    return False

def add_entry(message: str, category: str = None) -> None:
    brag_doc = get_brag_doc_path()
    now = datetime.now().strftime(TIMESTAMP_FORMAT)
    entry = BragEntry(timestamp=now, message=message, category=category)
    with open(brag_doc, "a") as f:
        if category:
            f.write(f"- [{entry.timestamp}] {CATEGORY_FORMAT.format(category=category)} {entry.message}\n")
        else:
            f.write(f"- [{entry.timestamp}] {entry.message}\n")

def read_history() -> List[str]:
    brag_doc = get_brag_doc_path()
    if not os.path.exists(brag_doc):
        return []
    with open(brag_doc, "r") as f:
        return f.readlines()

def purge_entries_between(start_date: str, end_date: str) -> int:
    """
    Purge brag doc entries between start_date and end_date (inclusive).
    Dates should be in 'YYYY-MM-DD' format.
    Returns the number of entries removed.
    """
    brag_doc = get_brag_doc_path()
    if not os.path.exists(brag_doc):
        return 0
    with open(brag_doc, "r") as f:
        lines = f.readlines()
    header = []
    entries = []
    for line in lines:
        if line.startswith("- ["):
            entries.append(line)
        else:
            header.append(line)
    start_dt = datetime.strptime(start_date, DATE_FORMAT).date()
    end_dt = datetime.strptime(end_date, DATE_FORMAT).date()
    kept = []
    removed = 0
    for entry in entries:
        try:
            ts = entry.split(']')[0][3:]
            entry_dt = datetime.strptime(ts, TIMESTAMP_FORMAT).date()
            if start_dt <= entry_dt <= end_dt:
                removed += 1
                continue
        except Exception:
            pass
        kept.append(entry)
    with open(brag_doc, "w") as f:
        f.writelines(header + kept)
    return removed

def init_brag_repo() -> str:
    """
    Initialize a git repo in the bragdoc's directory (if not already a repo) and create the bragdoc there.
    Returns the path to the bragdoc.
    """
    brag_doc = get_brag_doc_path()
    brag_dir = os.path.dirname(brag_doc)
    os.makedirs(brag_dir, exist_ok=True)
    # Initialize git repo if not present
    if not os.path.exists(os.path.join(brag_dir, ".git")):
        import git
        repo = git.Repo.init(brag_dir)
    else:
        repo = git.Repo(brag_dir)
    # Create bragdoc if not present
    if not os.path.exists(brag_doc):
        with open(brag_doc, "w") as f:
            f.write(BRAG_DOC_HEADER)
        repo.git.add(brag_doc)
        repo.index.commit(GIT_INIT_COMMIT_MESSAGE)
    return brag_doc
