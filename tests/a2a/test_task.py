"""
Tests for A2A Task lifecycle management.

Tests cover:
- Task state transitions
- Parent-child coordination
- Status callbacks
- Cascade operations
- Error handling
"""

import pytest
from sixspec.a2a import Task, TaskStatus, StatusUpdate


def test_task_creation():
    """Test task is created in PENDING state."""
    task = Task("test-task")

    assert task.task_id == "test-task"
    assert task.status == TaskStatus.PENDING
    assert task.result is None
    assert task.error is None
    assert len(task.children) == 0


def test_task_id_generation():
    """Test task ID is generated if not provided."""
    task = Task()

    assert task.task_id is not None
    assert task.task_id.startswith("task-")


def test_start_transition():
    """Test PENDING → RUNNING transition."""
    task = Task()
    task.start()

    assert task.status == TaskStatus.RUNNING


def test_cannot_start_running_task():
    """Test cannot start already running task."""
    task = Task()
    task.start()

    with pytest.raises(RuntimeError, match="Cannot start"):
        task.start()


def test_pause_transition():
    """Test RUNNING → PAUSED transition."""
    task = Task()
    task.start()
    task.pause()

    assert task.status == TaskStatus.PAUSED


def test_cannot_pause_pending():
    """Test cannot pause pending task."""
    task = Task()

    with pytest.raises(RuntimeError, match="Cannot pause"):
        task.pause()


def test_resume_transition():
    """Test PAUSED → RUNNING transition."""
    task = Task()
    task.start()
    task.pause()
    task.resume()

    assert task.status == TaskStatus.RUNNING


def test_cannot_resume_running():
    """Test cannot resume running task."""
    task = Task()
    task.start()

    with pytest.raises(RuntimeError, match="Cannot resume"):
        task.resume()


def test_complete_transition():
    """Test RUNNING → COMPLETED transition."""
    task = Task()
    task.start()
    task.complete("Success!")

    assert task.status == TaskStatus.COMPLETED
    assert task.result == "Success!"


def test_fail_transition():
    """Test RUNNING → FAILED transition."""
    task = Task()
    task.start()
    task.fail("Error occurred")

    assert task.status == TaskStatus.FAILED
    assert task.error == "Error occurred"


def test_cannot_complete_terminal():
    """Test cannot complete already terminal task."""
    task = Task()
    task.start()
    task.complete("Done")

    with pytest.raises(RuntimeError, match="terminal"):
        task.complete("Done again")


def test_parent_child_relationship():
    """Test parent-child task coordination."""
    parent = Task("parent")
    child = Task("child", parent=parent)

    assert child.parent == parent
    assert child in parent.children


def test_add_child():
    """Test manually adding child task."""
    parent = Task()
    child = Task()

    parent.add_child(child)

    assert child in parent.children
    # Adding same child again should not duplicate
    parent.add_child(child)
    assert parent.children.count(child) == 1


def test_status_callback():
    """Test status change callbacks."""
    task = Task()
    updates = []

    def track_update(update):
        updates.append(update)

    task.on_status_change(track_update)

    # Trigger status changes
    task.start()
    task.pause()

    assert len(updates) == 2
    assert updates[0].status == TaskStatus.RUNNING
    assert updates[1].status == TaskStatus.PAUSED


def test_cascade_pause_to_children():
    """Test pause cascades to all children."""
    parent = Task()
    child1 = Task(parent=parent)
    child2 = Task(parent=parent)

    # Start all
    parent.start()
    child1.start()
    child2.start()

    # Pause parent
    parent.pause()

    # All should be paused
    assert parent.status == TaskStatus.PAUSED
    assert child1.status == TaskStatus.PAUSED
    assert child2.status == TaskStatus.PAUSED


def test_cascade_resume_to_children():
    """Test resume cascades to children."""
    parent = Task()
    child1 = Task(parent=parent)
    child2 = Task(parent=parent)

    # Start and pause all
    parent.start()
    child1.start()
    child2.start()
    parent.pause()

    # Resume parent
    parent.resume()

    # All should be running
    assert parent.status == TaskStatus.RUNNING
    assert child1.status == TaskStatus.RUNNING
    assert child2.status == TaskStatus.RUNNING


def test_stream_status():
    """Test status streaming."""
    task = Task()
    task.start()

    # Get one status update
    stream = task.stream_status(metadata={"progress": 50})
    update = next(stream)

    assert update.task_id == task.task_id
    assert update.status == TaskStatus.RUNNING
    assert update.metadata["progress"] == 50


def test_task_to_dict():
    """Test task serialization."""
    parent = Task("parent")
    child = Task("child", parent=parent)

    parent.start()

    data = parent.to_dict()

    assert data["task_id"] == "parent"
    assert data["status"] == "running"
    assert "child" in data["children"]


def test_status_update_creation():
    """Test StatusUpdate dataclass."""
    update = StatusUpdate(
        task_id="test-task",
        status=TaskStatus.COMPLETED,
        result="Success",
        metadata={"progress": 100}
    )

    assert update.task_id == "test-task"
    assert update.status == TaskStatus.COMPLETED
    assert update.result == "Success"
    assert update.metadata["progress"] == 100


def test_status_update_default_metadata():
    """Test StatusUpdate initializes metadata dict."""
    update = StatusUpdate(
        task_id="test",
        status=TaskStatus.RUNNING
    )

    assert update.metadata == {}


def test_task_status_is_terminal():
    """Test terminal state detection."""
    assert TaskStatus.COMPLETED.is_terminal()
    assert TaskStatus.FAILED.is_terminal()
    assert not TaskStatus.RUNNING.is_terminal()
    assert not TaskStatus.PAUSED.is_terminal()
    assert not TaskStatus.PENDING.is_terminal()


def test_task_status_can_pause():
    """Test can_pause() method."""
    assert TaskStatus.RUNNING.can_pause()
    assert not TaskStatus.PENDING.can_pause()
    assert not TaskStatus.PAUSED.can_pause()
    assert not TaskStatus.COMPLETED.can_pause()


def test_task_status_can_resume():
    """Test can_resume() method."""
    assert TaskStatus.PAUSED.can_resume()
    assert not TaskStatus.PENDING.can_resume()
    assert not TaskStatus.RUNNING.can_resume()
    assert not TaskStatus.COMPLETED.can_resume()


def test_callback_error_does_not_break_task():
    """Test that callback errors don't break task execution."""
    task = Task()

    def bad_callback(update):
        raise ValueError("Callback error")

    task.on_status_change(bad_callback)

    # Should not raise despite bad callback
    task.start()
    assert task.status == TaskStatus.RUNNING


def test_deep_hierarchy_cascade():
    """Test cascade operations in deep hierarchy."""
    # Create 4-level hierarchy
    L1 = Task("L1")
    L2 = Task("L2", parent=L1)
    L3 = Task("L3", parent=L2)
    L4 = Task("L4", parent=L3)

    # Start all
    L1.start()
    L2.start()
    L3.start()
    L4.start()

    # Pause from top
    L1.pause()

    # All should be paused
    assert L1.status == TaskStatus.PAUSED
    assert L2.status == TaskStatus.PAUSED
    assert L3.status == TaskStatus.PAUSED
    assert L4.status == TaskStatus.PAUSED

    # Resume from top
    L1.resume()

    # All should be running
    assert L1.status == TaskStatus.RUNNING
    assert L2.status == TaskStatus.RUNNING
    assert L3.status == TaskStatus.RUNNING
    assert L4.status == TaskStatus.RUNNING
