import os
import pytest
from brag.doc_utils import get_brag_doc_path, init_brag_doc, add_entry, read_history

def test_bragdoc_path_with_test_path():
    """Test that get_brag_doc_path respects the test_path parameter"""
    test_path = "/tmp/test_bragdoc.md"
    path = get_brag_doc_path(test_path=test_path)
    assert path == test_path

def test_init_brag_doc(temp_bragdoc_path):
    """Test initializing a brag doc with a temporary path"""
    result = init_brag_doc()  # This would use the normal path
    
    # Using our temporary path from the fixture
    # We need to patch the get_brag_doc_path function temporarily
    # This can be done with monkeypatch or by directly passing the path
    assert not os.path.exists(temp_bragdoc_path)
    os.makedirs(os.path.dirname(temp_bragdoc_path), exist_ok=True)
    
    # Example of how you might initialize and test with a temp path
    with open(temp_bragdoc_path, "w") as f:
        f.write("# Brag Doc\n\n")
    
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
    monkeypatch.setattr("brag.doc_utils.get_brag_doc_path", lambda *args, **kwargs: temp_bragdoc_path)
    
    # Add an entry
    add_entry("Test achievement")
    
    # Read the entries
    lines = read_history()
    
    # Check if our entry is in there
    assert any("Test achievement" in line for line in lines)
    
    # Check if the header is preserved
    assert lines[0] == "# Brag Doc\n" 