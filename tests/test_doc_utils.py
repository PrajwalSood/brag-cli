import os
import pytest
from brag.doc_utils import get_brag_doc_path, init_brag_doc, add_entry, read_history

def test_bragdoc_path_with_test_path():
    """Test that get_brag_doc_path respects the test_path parameter"""
    test_path = "/tmp/test_bragdoc.md"
    path = get_brag_doc_path(test_path)
    assert path == test_path

def test_init_brag_doc(temp_bragdoc_path, monkeypatch):
    """Test initializing a brag doc with a temporary path"""
    # Monkeypatch the get_brag_doc_path function to return our temp path
    monkeypatch.setattr("brag.doc_utils.get_brag_doc_path", lambda *args: temp_bragdoc_path)
    
    # Now initialize the doc using our patched function
    result = init_brag_doc()
    assert result == True  # Should succeed because the file didn't exist before
    
    # Verify the file was created
    assert os.path.exists(temp_bragdoc_path)
    
    # Read from the temp file
    with open(temp_bragdoc_path, "r") as f:
        content = f.read()
    
    assert content == "# Brag Doc\n\n"

def test_add_and_read_entries(monkeypatch, temp_bragdoc_path):
    """Test adding and reading entries with a temporary bragdoc"""
    # First initialize the brag doc
    os.makedirs(os.path.dirname(temp_bragdoc_path), exist_ok=True)
    with open(temp_bragdoc_path, "w") as f:
        f.write("# Brag Doc\n\n")
    
    # Monkeypatch the get_brag_doc_path function to return our temp path
    monkeypatch.setattr("brag.doc_utils.get_brag_doc_path", lambda *args: temp_bragdoc_path)
    
    # Add an entry
    add_entry("Test achievement")
    
    # Read the entries
    lines = read_history()
    
    # Check if our entry is in there
    assert any("Test achievement" in line for line in lines)
    
    # Check if the header is preserved
    assert lines[0] == "# Brag Doc\n"

def test_testing_mode_uses_test_dir():
    """Test that when IS_TESTING is True, get_brag_doc_path uses TEST_DIR"""
    from brag import constants
    
    # This test should automatically use the test directory due to the autouse fixture
    path = get_brag_doc_path()
    
    # The path should be in the test directory
    assert constants.TEST_DIR in path
    assert path.endswith("bragdoc.md") 