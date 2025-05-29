import os
import pytest
import tempfile
import shutil
from brag import constants

@pytest.fixture(autouse=True)
def enable_testing_mode():
    """Enable testing mode for all tests."""
    # Store original value
    original_is_testing = constants.IS_TESTING
    original_test_dir = constants.TEST_DIR
    
    # Create a temporary directory for this test
    temp_dir = tempfile.mkdtemp()
    
    # Enable testing mode and set test directory
    constants.IS_TESTING = True
    constants.TEST_DIR = temp_dir
    
    yield temp_dir
    
    # Clean up
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    # Restore original values
    constants.IS_TESTING = original_is_testing
    constants.TEST_DIR = original_test_dir

@pytest.fixture
def temp_bragdoc_path():
    """
    Fixture that creates a temporary directory and returns a path to a bragdoc file within it.
    This allows tests to use a temporary bragdoc instead of the real one.
    """
    # Create a temp dir that will be automatically cleaned up
    temp_dir = tempfile.mkdtemp()
    bragdoc_path = os.path.join(temp_dir, "bragdoc.md")
    
    yield bragdoc_path
    
    # Clean up temp dir and all its contents
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

@pytest.fixture
def patch_brag_doc_path(monkeypatch):
    """
    Fixture that allows patching the get_brag_doc_path function to return a specific path.
    Usage: patch_brag_doc_path(some_path) will ensure brag functions use this path.
    """
    def _patch(path):
        monkeypatch.setattr("brag.doc_utils.get_brag_doc_path", lambda *args: path)
        # Also make sure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path
    
    return _patch

@pytest.fixture
def isolated_brag_env(temp_bragdoc_path, patch_brag_doc_path):
    """
    Comprehensive fixture that sets up an isolated environment for brag tests.
    - Creates a temporary bragdoc path
    - Patches all functions to use this path
    - Creates needed directories
    - Cleans up automatically
    """
    # Set up the environment with our temp path
    patch_brag_doc_path(temp_bragdoc_path)
    
    # Make sure the parent dir exists
    os.makedirs(os.path.dirname(temp_bragdoc_path), exist_ok=True)
    
    # Ready for testing
    yield temp_bragdoc_path 