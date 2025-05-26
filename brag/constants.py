import os

# File paths and names
BRAG_DOC_FILENAME = "bragdoc.md"
CATEGORY_FILE_NAME = ".brag_category"
PROFILE_FILE_NAME = ".brag_profile.json"

# Testing paths
TEST_BRAG_DOC_PATH = "TEST_BRAG_DOC_PATH"

# File system paths by OS
WINDOWS_BASE_PATH = "APPDATA"
DARWIN_APP_SUPPORT_PATH = os.path.join("Library", "Application Support")
LINUX_DATA_PATH = os.path.join(".local", "share")
XDG_DATA_HOME_ENV = "XDG_DATA_HOME"

# Brag doc format
BRAG_DOC_HEADER = "# Brag Doc\n\n"
BRAG_ENTRY_PREFIX = "- ["
CATEGORY_FORMAT = "[{category}]"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

# Git related
GIT_COMMIT_MESSAGE = "Update brag doc"
GIT_INIT_COMMIT_MESSAGE = "Initialize brag doc"

# Ollama API
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

# Profile related
PROFILE_FIELDS = [
    "name", "title", "summary", "skills", "experience", "education", 
    "contact.email", "contact.phone", "contact.linkedin", "contact.github"
] 