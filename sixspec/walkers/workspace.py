"""
Workspace: Isolated execution environment for walkers.

This module provides workspace isolation for DiltsWalker instances,
similar to git worktrees. Each walker gets its own isolated space
for execution without interfering with siblings.

Key Features:
- Isolated file system paths
- Independent memory storage
- Clean separation between parallel executions
- Easy cleanup on completion or failure

Example:
    >>> workspace = Workspace("Walker-L3-001")
    >>> workspace.path
    PosixPath('/tmp/sixspec/Walker-L3-001')
    >>> workspace.set("key", "value")
    >>> workspace.get("key")
    'value'
"""

import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional


class Workspace:
    """
    Isolated workspace for each walker (like git worktree).

    Each walker gets its own workspace to:
    - Store intermediate results
    - Maintain execution state
    - Avoid interfering with siblings
    - Enable easy rollback on failure

    Attributes:
        walker_id: Unique identifier for the walker
        path: Path to workspace directory
        memory: Key-value store for walker state

    Example:
        >>> ws = Workspace("Walker-L3-001")
        >>> ws.set("progress", {"step": 1, "status": "running"})
        >>> ws.get("progress")
        {'step': 1, 'status': 'running'}
        >>> ws.cleanup()  # Remove workspace directory
    """

    def __init__(self, walker_id: str, base_path: Optional[Path] = None):
        """
        Initialize a workspace for a walker.

        Args:
            walker_id: Unique identifier for this walker
            base_path: Optional base directory (defaults to temp directory)

        Example:
            >>> ws = Workspace("Walker-L3-001")
            >>> ws.walker_id
            'Walker-L3-001'
        """
        self.walker_id = walker_id
        self.memory: Dict[str, Any] = {}
        self.path = self.create_workspace_dir(base_path)

    def create_workspace_dir(self, base_path: Optional[Path] = None) -> Path:
        """
        Create isolated directory for this walker.

        Creates a new directory under the base path (or temp directory)
        with the walker's ID. If the directory already exists, uses it.

        Args:
            base_path: Optional base directory for workspaces

        Returns:
            Path to the created workspace directory

        Example:
            >>> ws = Workspace("test-walker")
            >>> ws.path.exists()
            True
            >>> ws.path.name
            'test-walker'
        """
        if base_path is None:
            base_path = Path(tempfile.gettempdir()) / "sixspec"

        workspace_path = base_path / self.walker_id
        workspace_path.mkdir(parents=True, exist_ok=True)
        return workspace_path

    def set(self, key: str, value: Any) -> None:
        """
        Store value in workspace memory.

        Args:
            key: Key to store value under
            value: Value to store (any Python object)

        Example:
            >>> ws = Workspace("test")
            >>> ws.set("result", {"success": True})
            >>> ws.memory["result"]
            {'success': True}
        """
        self.memory[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve value from workspace memory.

        Args:
            key: Key to retrieve
            default: Default value if key not found

        Returns:
            Stored value or default

        Example:
            >>> ws = Workspace("test")
            >>> ws.set("key", "value")
            >>> ws.get("key")
            'value'
            >>> ws.get("missing", "default")
            'default'
        """
        return self.memory.get(key, default)

    def has(self, key: str) -> bool:
        """
        Check if key exists in workspace memory.

        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise

        Example:
            >>> ws = Workspace("test")
            >>> ws.set("key", "value")
            >>> ws.has("key")
            True
            >>> ws.has("missing")
            False
        """
        return key in self.memory

    def cleanup(self) -> None:
        """
        Remove workspace directory and clear memory.

        This method should be called when the walker completes or fails
        to clean up resources.

        Example:
            >>> ws = Workspace("test")
            >>> ws.path.exists()
            True
            >>> ws.cleanup()
            >>> ws.path.exists()
            False
        """
        if self.path.exists():
            shutil.rmtree(self.path)
        self.memory.clear()

    def write_file(self, filename: str, content: str) -> Path:
        """
        Write a file to the workspace.

        Args:
            filename: Name of file to write
            content: Content to write

        Returns:
            Path to written file

        Example:
            >>> ws = Workspace("test")
            >>> file_path = ws.write_file("output.txt", "Hello World")
            >>> file_path.read_text()
            'Hello World'
        """
        file_path = self.path / filename
        file_path.write_text(content)
        return file_path

    def read_file(self, filename: str) -> str:
        """
        Read a file from the workspace.

        Args:
            filename: Name of file to read

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: If file doesn't exist

        Example:
            >>> ws = Workspace("test")
            >>> ws.write_file("test.txt", "content")
            >>> ws.read_file("test.txt")
            'content'
        """
        file_path = self.path / filename
        return file_path.read_text()

    def list_files(self) -> list[Path]:
        """
        List all files in the workspace.

        Returns:
            List of file paths in workspace

        Example:
            >>> ws = Workspace("test")
            >>> ws.write_file("file1.txt", "a")
            >>> ws.write_file("file2.txt", "b")
            >>> len(ws.list_files())
            2
        """
        return list(self.path.glob("*"))