import os
import json
from typing import Dict, Optional, Any
import platform
from brag.constants import (
    PROFILE_FILE_NAME,
    WINDOWS_BASE_PATH, DARWIN_APP_SUPPORT_PATH, LINUX_DATA_PATH, XDG_DATA_HOME_ENV,
    TEST_BRAG_DOC_PATH
)

def get_profile_path(test_path: str = None) -> str:
    """
    Get the path to the profile file.
    
    Args:
        test_path: Optional path for testing purposes. If None, normal path resolution is used.
        
    Returns:
        Path to the profile file.
    """
    # Use explicit test path if provided
    if test_path:
        return os.path.join(os.path.dirname(test_path), PROFILE_FILE_NAME)
        
    # Use environment variable test path if set
    if TEST_BRAG_DOC_PATH:
        return os.path.join(os.path.dirname(TEST_BRAG_DOC_PATH), PROFILE_FILE_NAME)
        
    # Normal path resolution based on OS
    home = os.path.expanduser("~")
    if platform.system() == "Windows":
        base = os.environ.get(WINDOWS_BASE_PATH, home)
        return os.path.join(os.path.dirname(base), PROFILE_FILE_NAME)
    elif platform.system() == "Darwin":
        return os.path.join(home, DARWIN_APP_SUPPORT_PATH, PROFILE_FILE_NAME)
    else:  # Linux and others
        xdg = os.environ.get(XDG_DATA_HOME_ENV, os.path.join(home, LINUX_DATA_PATH))
        return os.path.join(xdg, PROFILE_FILE_NAME)

def init_profile() -> bool:
    """Initialize a profile file if it doesn't exist."""
    profile_path = get_profile_path()
    if not os.path.exists(profile_path):
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)
        default_profile = {
            "name": "",
            "title": "",
            "skills": [],
            "experience": [],
            "education": [],
            "contact": {
                "email": "",
                "phone": "",
                "linkedin": "",
                "github": ""
            },
            "summary": ""
        }
        save_profile(default_profile)
        return True
    return False

def save_profile(profile_data: Dict[str, Any]) -> None:
    """Save profile data to file."""
    profile_path = get_profile_path()
    with open(profile_path, "w") as f:
        json.dump(profile_data, f, indent=2)

def get_profile() -> Dict[str, Any]:
    """Get profile data from file."""
    profile_path = get_profile_path()
    if not os.path.exists(profile_path):
        init_profile()
        return get_profile()
    
    with open(profile_path, "r") as f:
        return json.load(f)

def update_profile_field(field: str, value: Any) -> None:
    """Update a specific profile field."""
    profile = get_profile()
    
    # Handle nested fields like "contact.email"
    if "." in field:
        parts = field.split(".")
        current = profile
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    else:
        profile[field] = value
    
    save_profile(profile)

def add_list_item(field: str, item: Any) -> None:
    """Add an item to a list field in the profile."""
    profile = get_profile()
    
    # Handle nested fields
    if "." in field:
        parts = field.split(".")
        current = profile
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        if parts[-1] not in current:
            current[parts[-1]] = []
        if not isinstance(current[parts[-1]], list):
            current[parts[-1]] = [current[parts[-1]]]
        current[parts[-1]].append(item)
    else:
        if field not in profile:
            profile[field] = []
        if not isinstance(profile[field], list):
            profile[field] = [profile[field]]
        profile[field].append(item)
    
    save_profile(profile)

def remove_list_item(field: str, index: int) -> Optional[Any]:
    """Remove an item from a list field by index."""
    profile = get_profile()
    
    # Handle nested fields
    if "." in field:
        parts = field.split(".")
        current = profile
        for part in parts[:-1]:
            if part not in current:
                return None
            current = current[part]
        if parts[-1] not in current or not isinstance(current[parts[-1]], list):
            return None
        if index >= len(current[parts[-1]]):
            return None
        removed = current[parts[-1]].pop(index)
    else:
        if field not in profile or not isinstance(profile[field], list):
            return None
        if index >= len(profile[field]):
            return None
        removed = profile[field].pop(index)
    
    save_profile(profile)
    return removed 