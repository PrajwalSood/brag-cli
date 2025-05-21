import os
import pytest
import tempfile

@pytest.fixture
def temp_bragdoc_path():
    """
    Fixture that creates a temporary directory and returns a path to a bragdoc file within it.
    This allows tests to use a temporary bragdoc instead of the real one.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        bragdoc_path = os.path.join(temp_dir, "bragdoc.md")
        yield bragdoc_path 