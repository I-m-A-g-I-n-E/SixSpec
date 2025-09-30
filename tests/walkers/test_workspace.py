"""
Tests for Workspace isolation.

Tests cover:
- Workspace creation
- Memory storage
- File operations
- Cleanup
- Isolation between workspaces
"""

import pytest
from pathlib import Path
from sixspec.walkers.workspace import Workspace


def test_workspace_creation():
    """Test that workspace is created with proper structure."""
    ws = Workspace("test-walker-001")

    assert ws.walker_id == "test-walker-001"
    assert ws.path.exists()
    assert ws.path.is_dir()
    assert "test-walker-001" in str(ws.path)

    # Cleanup
    ws.cleanup()


def test_workspace_memory_storage():
    """Test memory key-value storage."""
    ws = Workspace("test-memory")

    # Set values
    ws.set("key1", "value1")
    ws.set("key2", {"nested": "dict"})
    ws.set("key3", 123)

    # Get values
    assert ws.get("key1") == "value1"
    assert ws.get("key2") == {"nested": "dict"}
    assert ws.get("key3") == 123

    # Get with default
    assert ws.get("missing", "default") == "default"

    # Has check
    assert ws.has("key1") is True
    assert ws.has("missing") is False

    # Cleanup
    ws.cleanup()


def test_workspace_file_operations():
    """Test file read/write operations."""
    ws = Workspace("test-files")

    # Write file
    file_path = ws.write_file("test.txt", "Hello World")
    assert file_path.exists()
    assert file_path.read_text() == "Hello World"

    # Read file
    content = ws.read_file("test.txt")
    assert content == "Hello World"

    # List files
    ws.write_file("file1.txt", "content1")
    ws.write_file("file2.txt", "content2")
    files = ws.list_files()
    assert len(files) >= 3  # At least test.txt, file1.txt, file2.txt

    # Cleanup
    ws.cleanup()


def test_workspace_cleanup():
    """Test that cleanup removes workspace."""
    ws = Workspace("test-cleanup")
    path = ws.path

    # Set some data
    ws.set("key", "value")
    ws.write_file("test.txt", "content")

    assert path.exists()
    assert ws.has("key")

    # Cleanup
    ws.cleanup()

    # Path should not exist
    assert not path.exists()
    # Memory should be cleared
    assert not ws.has("key")


def test_workspace_isolation():
    """Test that workspaces are isolated from each other."""
    ws1 = Workspace("walker-001")
    ws2 = Workspace("walker-002")

    # Different paths
    assert ws1.path != ws2.path

    # Independent memory
    ws1.set("shared_key", "value1")
    ws2.set("shared_key", "value2")
    assert ws1.get("shared_key") == "value1"
    assert ws2.get("shared_key") == "value2"

    # Independent files
    ws1.write_file("data.txt", "data1")
    ws2.write_file("data.txt", "data2")
    assert ws1.read_file("data.txt") == "data1"
    assert ws2.read_file("data.txt") == "data2"

    # Cleanup
    ws1.cleanup()
    ws2.cleanup()


def test_workspace_with_custom_base_path(tmp_path):
    """Test workspace creation with custom base path."""
    custom_base = tmp_path / "custom_workspaces"
    ws = Workspace("test-custom", base_path=custom_base)

    assert ws.path.parent == custom_base
    assert ws.path.exists()
    assert "test-custom" in str(ws.path)

    # Cleanup
    ws.cleanup()


def test_workspace_read_nonexistent_file():
    """Test reading a file that doesn't exist."""
    ws = Workspace("test-nonexistent")

    with pytest.raises(FileNotFoundError):
        ws.read_file("nonexistent.txt")

    # Cleanup
    ws.cleanup()


def test_workspace_multiple_file_types():
    """Test workspace with different file types."""
    ws = Workspace("test-filetypes")

    # Write different types of files
    ws.write_file("text.txt", "plain text")
    ws.write_file("data.json", '{"key": "value"}')
    ws.write_file("code.py", "def hello():\n    return 'world'")

    # Read them back
    assert ws.read_file("text.txt") == "plain text"
    assert ws.read_file("data.json") == '{"key": "value"}'
    assert "def hello" in ws.read_file("code.py")

    # Cleanup
    ws.cleanup()


def test_workspace_memory_types():
    """Test that workspace memory handles various types."""
    ws = Workspace("test-types")

    # Store different types
    ws.set("string", "text")
    ws.set("int", 42)
    ws.set("float", 3.14)
    ws.set("bool", True)
    ws.set("list", [1, 2, 3])
    ws.set("dict", {"a": 1, "b": 2})
    ws.set("none", None)

    # Retrieve and verify types
    assert isinstance(ws.get("string"), str)
    assert isinstance(ws.get("int"), int)
    assert isinstance(ws.get("float"), float)
    assert isinstance(ws.get("bool"), bool)
    assert isinstance(ws.get("list"), list)
    assert isinstance(ws.get("dict"), dict)
    assert ws.get("none") is None

    # Cleanup
    ws.cleanup()


def test_workspace_reuse_existing_directory():
    """Test that workspace can use existing directory."""
    ws1 = Workspace("test-reuse")
    path = ws1.path

    # Write a file
    ws1.write_file("existing.txt", "content")

    # Create another workspace with same ID
    ws2 = Workspace("test-reuse")

    # Should use same directory
    assert ws2.path == path
    # File should still exist
    assert ws2.read_file("existing.txt") == "content"

    # Cleanup
    ws1.cleanup()


def test_workspace_empty_list_files():
    """Test listing files in empty workspace."""
    ws = Workspace("test-empty")

    files = ws.list_files()
    assert isinstance(files, list)
    assert len(files) == 0

    # Cleanup
    ws.cleanup()