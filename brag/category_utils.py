import difflib
from typing import List, Optional, Tuple
from collections import Counter
import os

def extract_categories_from_history(history_lines: List[str]) -> List[str]:
    """
    Extract unique categories from brag history lines.
    Assumes lines are in the format: '- [timestamp] [category] message' or '- [timestamp] message'.
    """
    categories = set()
    for line in history_lines:
        if line.startswith("- ["):
            # Try to extract category (assume category is in square brackets after timestamp)
            parts = line.split("] ", 1)
            if len(parts) == 2:
                rest = parts[1]
                if rest.startswith("["):
                    cat_end = rest.find("]")
                    if cat_end != -1:
                        category = rest[1:cat_end].strip()
                        if category:
                            categories.add(category)
    return list(categories)

def parse_brag_line(line: str) -> Tuple[Optional[str], str]:
    """
    Parse a brag line and return (category, message).
    """
    if not line.startswith("- ["):
        return (None, "")
    # Remove timestamp
    parts = line.split("] ", 1)
    if len(parts) != 2:
        return (None, "")
    rest = parts[1]
    if rest.startswith("["):
        cat_end = rest.find("]")
        if cat_end != -1:
            category = rest[1:cat_end].strip()
            message = rest[cat_end+2:].strip()
            return (category, message)
    # No category
    return (None, rest.strip())

def find_closest_category(new_message: str, history_lines: List[str], cutoff: float = 0.6) -> Optional[str]:
    """
    Find the most likely category for new_message by majority voting among the top 3 most similar previous brag messages.
    Returns the most common category if there is a majority, else None.
    """
    # Build a list of (category, message) from history
    samples = [parse_brag_line(line) for line in history_lines if line.startswith("- [")]
    messages = [msg for cat, msg in samples if msg]
    if not messages:
        return None
    # Find top 3 closest messages
    matches = difflib.get_close_matches(new_message, messages, n=3, cutoff=cutoff)
    if not matches:
        return None
    # Get categories for these messages
    matched_categories = []
    for match in matches:
        for cat, msg in samples:
            if msg == match:
                if cat:
                    matched_categories.append(cat)
                break
    if not matched_categories:
        return None
    # Majority vote
    counter = Counter(matched_categories)
    most_common, count = counter.most_common(1)[0]
    if count > 1 or len(counter) == 1:
        return most_common
    return None

def get_category_file_path() -> str:
    """Return the path to the .brag_category file in the brag doc directory."""
    from brag.doc_utils import get_brag_doc_path
    brag_doc = get_brag_doc_path()
    return os.path.join(os.path.dirname(brag_doc), ".brag_category")

def set_current_category(category: str) -> None:
    """Set the current category (persisted in .brag_category)."""
    path = get_category_file_path()
    with open(path, "w") as f:
        f.write(category.strip() + "\n")

def get_current_category() -> Optional[str]:
    """Get the current category if set, else None."""
    path = get_category_file_path()
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip() or None
    return None

def unset_current_category() -> None:
    """Unset the current category (remove .brag_category file)."""
    path = get_category_file_path()
    if os.path.exists(path):
        os.remove(path)

def change_current_category(new_category: str) -> None:
    """Change the current category (overwrite .brag_category)."""
    set_current_category(new_category)

def list_categories(history_lines: List[str]) -> list:
    """Return a list of unique categories from brag history."""
    return extract_categories_from_history(history_lines)

def select_category_by_index(history_lines: List[str], index: int) -> str:
    """Return the category at the given index from the list of unique categories."""
    categories = list_categories(history_lines)
    if not categories:
        raise ValueError("No categories found.")
    if index < 0 or index >= len(categories):
        raise IndexError(f"Index {index} out of range for categories list.")
    return categories[index] 