import os

# File paths and names
BRAG_DOC_FILENAME = "bragdoc.md"
CATEGORY_FILE_NAME = ".brag_category"

# Testing paths
TEST_BRAG_DOC_PATH = os.environ.get("TEST_BRAG_DOC_PATH", None)

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