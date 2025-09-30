"""
A2A-compatible Task implementation for lifecycle management.

This module provides a Task class that follows the Google A2A protocol
for agent task management, enabling graceful pause/resume and parent-child
coordination.
"""

import uuid
from typing import Any, Callable, List, Optional

from sixspec.a2a.status import StatusUpdate, TaskStatus


class Task:
    """
    A2A-compatible task with lifecycle management.

    Task implements the core A2A protocol for task lifecycle:
    - State transitions: pending → running → paused/completed/failed
    - Parent-child coordination: children notify parents of status changes
    - Graceful interruption: pause preserves state for later resume
    - Status streaming: real-time updates via callbacks

    Attributes:
        task_id: Unique identifier for this task
        status: Current task status
        result: Result data (when completed)
        error: Error message (when failed)
        parent: Optional parent task
        children: List of child tasks
        status_callbacks: Callbacks invoked on status change

    Example:
        >>> task = Task("my-task")
        >>> task.start()
        >>> task.status
        <TaskStatus.RUNNING: 'running'>
        >>> task.complete("done")
        >>> task.result
        'done'
    """

    def __init__(
        self,
        task_id: Optional[str] = None,
        parent: Optional['Task'] = None
    ):
        """
        Initialize a new task.

        Args:
            task_id: Optional task identifier (generated if not provided)
            parent: Optional parent task for hierarchical coordination
        """
        self.task_id = task_id or f"task-{uuid.uuid4().hex[:8]}"
        self.status = TaskStatus.PENDING
        self.result: Optional[Any] = None
        self.error: Optional[str] = None
        self.parent = parent
        self.children: List['Task'] = []
        self.status_callbacks: List[Callable[[StatusUpdate], None]] = []

        # If we have a parent, register with it
        if parent:
            parent.add_child(self)

    def add_child(self, child: 'Task') -> None:
        """
        Add a child task.

        Args:
            child: Child task to add
        """
        if child not in self.children:
            self.children.append(child)

    def on_status_change(self, callback: Callable[[StatusUpdate], None]) -> None:
        """
        Register a callback for status changes.

        Used for parent-child coordination: parent subscribes to child
        status updates to react to completion, failure, or pause events.

        Args:
            callback: Function called with StatusUpdate on status change

        Example:
            >>> parent = Task()
            >>> child = Task(parent=parent)
            >>> def handle_update(update):
            ...     print(f"Child status: {update.status}")
            >>> child.on_status_change(handle_update)
        """
        self.status_callbacks.append(callback)

    def _notify_status_change(self, metadata: Optional[dict] = None) -> None:
        """
        Notify callbacks of status change.

        Creates StatusUpdate and invokes all registered callbacks.
        Used for parent-child coordination and status streaming.

        Args:
            metadata: Optional metadata to include in update
        """
        update = StatusUpdate(
            task_id=self.task_id,
            status=self.status,
            result=self.result,
            error=self.error,
            metadata=metadata or {}
        )

        for callback in self.status_callbacks:
            try:
                callback(update)
            except Exception:
                # Don't let callback errors break task execution
                pass

    def start(self) -> None:
        """
        Start task execution.

        Transitions from PENDING to RUNNING.

        Raises:
            RuntimeError: If task is not in PENDING state

        Example:
            >>> task = Task()
            >>> task.start()
            >>> task.status
            <TaskStatus.RUNNING: 'running'>
        """
        if self.status != TaskStatus.PENDING:
            raise RuntimeError(
                f"Cannot start task in {self.status.value} state"
            )

        self.status = TaskStatus.RUNNING
        self._notify_status_change()

    def pause(self) -> None:
        """
        Pause task execution gracefully.

        Transitions from RUNNING to PAUSED. Preserves all task state
        for later resume. Cascade pause to all children.

        Raises:
            RuntimeError: If task is not RUNNING

        Example:
            >>> task = Task()
            >>> task.start()
            >>> task.pause()
            >>> task.status
            <TaskStatus.PAUSED: 'paused'>
        """
        if not self.status.can_pause():
            raise RuntimeError(
                f"Cannot pause task in {self.status.value} state"
            )

        self.status = TaskStatus.PAUSED
        self._notify_status_change()

        # Cascade pause to children
        for child in self.children:
            if child.status.can_pause():
                child.pause()

    def resume(self) -> None:
        """
        Resume task execution from paused state.

        Transitions from PAUSED to RUNNING. Restores full execution
        context. Resume children first (bottom-up).

        Raises:
            RuntimeError: If task is not PAUSED

        Example:
            >>> task = Task()
            >>> task.start()
            >>> task.pause()
            >>> task.resume()
            >>> task.status
            <TaskStatus.RUNNING: 'running'>
        """
        if not self.status.can_resume():
            raise RuntimeError(
                f"Cannot resume task in {self.status.value} state"
            )

        # Resume children first (bottom-up)
        for child in self.children:
            if child.status.can_resume():
                child.resume()

        self.status = TaskStatus.RUNNING
        self._notify_status_change()

    def complete(self, result: Any = None) -> None:
        """
        Mark task as completed successfully.

        Transitions to COMPLETED terminal state. Stores result.

        Args:
            result: Optional result data

        Raises:
            RuntimeError: If task is already in terminal state

        Example:
            >>> task = Task()
            >>> task.start()
            >>> task.complete("Success!")
            >>> task.status
            <TaskStatus.COMPLETED: 'completed'>
            >>> task.result
            'Success!'
        """
        if self.status.is_terminal():
            raise RuntimeError(
                f"Cannot complete task in terminal {self.status.value} state"
            )

        self.status = TaskStatus.COMPLETED
        self.result = result
        self._notify_status_change()

    def fail(self, error: str) -> None:
        """
        Mark task as failed.

        Transitions to FAILED terminal state. Stores error message.

        Args:
            error: Error message describing failure

        Raises:
            RuntimeError: If task is already in terminal state

        Example:
            >>> task = Task()
            >>> task.start()
            >>> task.fail("Connection timeout")
            >>> task.status
            <TaskStatus.FAILED: 'failed'>
            >>> task.error
            'Connection timeout'
        """
        if self.status.is_terminal():
            raise RuntimeError(
                f"Cannot fail task in terminal {self.status.value} state"
            )

        self.status = TaskStatus.FAILED
        self.error = error
        self._notify_status_change()

    def stream_status(self, metadata: Optional[dict] = None):
        """
        Generate status updates for streaming.

        Yields status updates while task is active. Used for real-time
        monitoring of task progress via gRPC or similar streaming protocols.

        Args:
            metadata: Optional metadata to include in updates

        Yields:
            StatusUpdate objects with current task state

        Example:
            >>> task = Task()
            >>> task.start()
            >>> for update in task.stream_status():
            ...     print(f"Status: {update.status}")
            ...     if update.status.is_terminal():
            ...         break
        """
        while not self.status.is_terminal():
            yield StatusUpdate(
                task_id=self.task_id,
                status=self.status,
                result=self.result,
                error=self.error,
                metadata=metadata or {}
            )

            # If paused or completed, stop streaming
            if self.status in {TaskStatus.PAUSED, TaskStatus.COMPLETED, TaskStatus.FAILED}:
                break

    def to_dict(self) -> dict:
        """
        Serialize task to dictionary.

        Returns:
            Dictionary representation of task state

        Example:
            >>> task = Task("my-task")
            >>> task.start()
            >>> task.to_dict()
            {'task_id': 'my-task', 'status': 'running', ...}
        """
        return {
            'task_id': self.task_id,
            'status': self.status.value,
            'result': self.result,
            'error': self.error,
            'children': [child.task_id for child in self.children],
        }
