"""
A2A (Agent-to-Agent) Protocol Integration for SixSpec.

This module provides an A2A-compatible task lifecycle management system
for graceful interruption, pause/resume, and hierarchical task coordination.

Key Components:
    - Task: A2A-compatible task with lifecycle states
    - TaskStatus: Enum for task states (pending, running, paused, completed, failed)
    - StatusUpdate: Status change notifications for parent-child coordination

Example:
    >>> from sixspec.a2a import Task, TaskStatus
    >>> task = Task("my-task")
    >>> task.start()
    >>> task.status
    <TaskStatus.RUNNING: 'running'>
    >>> task.pause()
    >>> task.status
    <TaskStatus.PAUSED: 'paused'>
"""

from sixspec.a2a.status import TaskStatus, StatusUpdate
from sixspec.a2a.task import Task

__all__ = ['Task', 'TaskStatus', 'StatusUpdate']
