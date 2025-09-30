"""
Status definitions for A2A task lifecycle.

This module defines status enums and update messages for the A2A protocol,
enabling task lifecycle management and parent-child coordination.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class TaskStatus(Enum):
    """
    A2A-compatible task lifecycle states.

    States follow the Google A2A protocol for agent task management:
    - PENDING: Task created but not yet started
    - RUNNING: Task actively executing
    - PAUSED: Task gracefully paused, can be resumed
    - COMPLETED: Task finished successfully
    - FAILED: Task encountered error and cannot continue

    Example:
        >>> status = TaskStatus.RUNNING
        >>> status.value
        'running'
    """
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

    def is_terminal(self) -> bool:
        """
        Check if this is a terminal state.

        Terminal states (COMPLETED, FAILED) cannot transition to other states.

        Returns:
            True if terminal state, False otherwise
        """
        return self in {TaskStatus.COMPLETED, TaskStatus.FAILED}

    def can_pause(self) -> bool:
        """
        Check if task can be paused from this state.

        Only RUNNING tasks can be paused.

        Returns:
            True if task can be paused, False otherwise
        """
        return self == TaskStatus.RUNNING

    def can_resume(self) -> bool:
        """
        Check if task can be resumed from this state.

        Only PAUSED tasks can be resumed.

        Returns:
            True if task can be resumed, False otherwise
        """
        return self == TaskStatus.PAUSED


@dataclass
class StatusUpdate:
    """
    Status update message for parent-child task coordination.

    When a child task changes status, it sends StatusUpdate to its parent
    via callback or streaming interface. This enables:
    - Real-time progress monitoring
    - Cascade operations (pause propagates to children)
    - Error propagation from child to parent

    Attributes:
        task_id: Identifier of the task
        status: New task status
        result: Optional result data (for completed tasks)
        error: Optional error message (for failed tasks)
        metadata: Additional context (progress %, current action, etc.)

    Example:
        >>> update = StatusUpdate(
        ...     task_id="child-task-1",
        ...     status=TaskStatus.COMPLETED,
        ...     result="Success",
        ...     metadata={"progress_pct": 100}
        ... )
        >>> update.status
        <TaskStatus.COMPLETED: 'completed'>
    """
    task_id: str
    status: TaskStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: dict = None

    def __post_init__(self):
        """Initialize metadata dict if not provided."""
        if self.metadata is None:
            self.metadata = {}
