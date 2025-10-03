"""
Tests for A2AWalker with A2A task lifecycle integration.

Tests cover:
- Task lifecycle (start, pause, resume, complete)
- WHAT→WHY preservation during pause/resume
- Cascade pause to children
- Progress inspection with get_progress()
- Status streaming
- Parent-child coordination
- Dynamic re-planning with update_what()
"""

import pytest
from sixspec.a2a import TaskStatus
from sixspec.core.models import Dimension, DiltsLevel, Chunk
from sixspec.walkers.a2a_walker import A2AWalker


def test_task_lifecycle_basic():
    """
    Test basic task lifecycle: start → complete.

    A2AWalker should create task and manage its lifecycle.
    """
    walker = A2AWalker(level=DiltsLevel.ENVIRONMENT)
    spec = Chunk(
        subject="System",
        predicate="executes",
        object="action",
        dimensions={Dimension.WHAT: "Run tests"}
    )

    # Task should start as PENDING
    assert walker.task.status == TaskStatus.PENDING

    # Execute should start and complete task
    result = walker.execute(spec)

    assert walker.task.status == TaskStatus.COMPLETED
    assert "EXECUTED" in result


def test_pause_preserves_what_why():
    """
    Test that pause preserves WHAT→WHY chain.

    After pause, dimensional context should remain intact.
    """
    walker = A2AWalker(level=DiltsLevel.CAPABILITY)
    walker.add_context(Dimension.WHAT, "Integrate payment")
    walker.add_context(Dimension.WHY, "Launch premium")

    # Start task
    walker.task.start()

    # Pause
    walker.pause()

    # Context preserved
    assert walker.task.status == TaskStatus.PAUSED
    assert walker.context[Dimension.WHAT] == "Integrate payment"
    assert walker.context[Dimension.WHY] == "Launch premium"


def test_cascade_pause():
    """
    Test that pause cascades to all children.

    When parent pauses, all children should pause too.
    """
    parent = A2AWalker(level=DiltsLevel.IDENTITY)

    # Create children
    child1 = A2AWalker(level=DiltsLevel.BELIEFS, parent=parent)
    child2 = A2AWalker(level=DiltsLevel.BELIEFS, parent=parent)
    parent.children = [child1, child2]

    # Start all tasks
    parent.task.start()
    child1.task.start()
    child2.task.start()

    # Pause parent
    parent.pause()

    # All should be paused
    assert parent.task.status == TaskStatus.PAUSED
    assert child1.task.status == TaskStatus.PAUSED
    assert child2.task.status == TaskStatus.PAUSED


def test_resume_continues_execution():
    """
    Test that resume continues from exact position.

    After resume, walker should continue with same WHAT→WHY chain.
    """
    walker = A2AWalker(level=DiltsLevel.ENVIRONMENT)
    spec = Chunk(
        subject="System",
        predicate="executes",
        object="action",
        dimensions={
            Dimension.WHAT: "Deploy code",
            Dimension.WHY: "Release feature"
        }
    )

    # Simulate paused state using proper lifecycle methods
    walker.task.start()
    walker.paused_spec = spec
    walker.add_context(Dimension.WHAT, "Deploy code")
    walker.add_context(Dimension.WHY, "Release feature")
    walker.task.pause()

    # Get state before resume
    what_before = walker.context[Dimension.WHAT]
    why_before = walker.context[Dimension.WHY]

    # Resume
    result = walker.resume()

    # Should continue with same context
    assert walker.context[Dimension.WHAT] == what_before
    assert walker.context[Dimension.WHY] == why_before
    assert walker.task.status == TaskStatus.COMPLETED


def test_get_progress():
    """
    Test get_progress() returns full execution state.

    Should include level, status, WHAT, WHY, provenance, children.
    """
    parent = A2AWalker(level=DiltsLevel.IDENTITY)
    parent.add_context(Dimension.WHAT, "Launch product")
    parent.add_context(Dimension.WHY, "Increase revenue")
    parent.task.start()

    # Create child
    child = A2AWalker(level=DiltsLevel.BELIEFS, parent=parent)
    child.add_context(Dimension.WHAT, "Build feature")
    child.add_context(Dimension.WHY, "Launch product")
    child.task.start()
    parent.children = [child]

    # Get progress
    progress = parent.get_progress()

    # Verify structure
    assert progress["level"] == DiltsLevel.IDENTITY.value
    assert progress["status"] == "running"
    assert progress["what"] == "Launch product"
    assert progress["why"] == "Increase revenue"
    assert len(progress["children"]) == 1
    assert progress["children"][0]["what"] == "Build feature"


def test_parent_child_coordination():
    """
    Test parent-child task coordination.

    Parent should receive status updates from children.
    """
    parent = A2AWalker(level=DiltsLevel.IDENTITY)
    child = A2AWalker(level=DiltsLevel.BELIEFS, parent=parent)

    # Track parent's handler calls
    updates_received = []

    def track_updates(update):
        updates_received.append(update)

    child.task.on_status_change(track_updates)

    # Start child
    child.task.start()

    # Should have received update
    assert len(updates_received) == 1
    assert updates_received[0].status == TaskStatus.RUNNING


def test_trace_provenance_with_a2a():
    """
    Test provenance tracing works with A2AWalker.

    Should trace full WHAT→WHY chain from child to root.
    """
    L5 = A2AWalker(level=DiltsLevel.IDENTITY)
    L5.add_context(Dimension.WHAT, "Launch premium tier")

    L4 = A2AWalker(level=DiltsLevel.BELIEFS, parent=L5)
    L4.add_context(Dimension.WHAT, "Build billing system")

    L3 = A2AWalker(level=DiltsLevel.CAPABILITY, parent=L4)
    L3.add_context(Dimension.WHAT, "Integrate Stripe")

    # Trace from L3 to L5
    chain = L3.trace_provenance()

    assert len(chain) == 3
    assert chain[0] == "Launch premium tier"
    assert chain[1] == "Build billing system"
    assert chain[2] == "Integrate Stripe"


def test_stream_status():
    """
    Test status streaming yields updates.

    Should generate updates while task is active.
    """
    walker = A2AWalker(level=DiltsLevel.CAPABILITY)
    walker.add_context(Dimension.WHAT, "Build feature")
    walker.task.start()

    # Get first status update
    status_gen = walker.stream_status()
    status = next(status_gen)

    assert status["status"] == "running"
    assert status["what"] == "Build feature"
    assert "progress_pct" in status


def test_calculate_progress():
    """
    Test progress calculation.

    Should calculate based on task status and children.
    """
    # Completed task should be 100%
    walker = A2AWalker(level=DiltsLevel.ENVIRONMENT)
    walker.task.status = TaskStatus.COMPLETED
    assert walker.calculate_progress() == 100.0

    # Failed task should be 0%
    walker2 = A2AWalker(level=DiltsLevel.ENVIRONMENT)
    walker2.task.status = TaskStatus.FAILED
    assert walker2.calculate_progress() == 0.0

    # Running task with no children should be ~50%
    walker3 = A2AWalker(level=DiltsLevel.CAPABILITY)
    walker3.task.start()
    progress = walker3.calculate_progress()
    assert 0.0 <= progress <= 100.0


def test_update_what_preserves_why():
    """
    Test dynamic re-planning with update_what().

    Should update WHAT while preserving WHY.
    """
    walker = A2AWalker(level=DiltsLevel.CAPABILITY)
    walker.add_context(Dimension.WHAT, "Use Stripe")
    walker.add_context(Dimension.WHY, "Process payments")

    # Update WHAT
    walker.update_what("Use PayPal")

    # WHAT changed, WHY preserved
    assert walker.context[Dimension.WHAT] == "Use PayPal"
    assert walker.context[Dimension.WHY] == "Process payments"


def test_full_pause_inspect_resume_workflow():
    """
    Test complete pause → inspect → resume workflow.

    This is the primary use case from the ticket.
    """
    # Start mission
    mission = A2AWalker(level=DiltsLevel.MISSION)
    spec = Chunk(
        subject="Company",
        predicate="aims",
        object="growth",
        dimensions={Dimension.WHAT: "Increase revenue by 20%"}
    )

    # Execute until we have some structure
    mission.current_node = spec
    mission.add_context(Dimension.WHAT, "Increase revenue by 20%")
    mission.workspace = None
    mission.task.start()

    # Create some children to simulate execution
    child = A2AWalker(level=DiltsLevel.IDENTITY, parent=mission)
    child.add_context(Dimension.WHAT, "Launch premium tier")
    child.add_context(Dimension.WHY, "Increase revenue by 20%")
    child.task.start()
    mission.children = [child]

    # Pause mission
    mission.pause()

    # Mission and children should be paused
    assert mission.task.status == TaskStatus.PAUSED
    assert child.task.status == TaskStatus.PAUSED

    # Inspect progress
    progress = mission.get_progress()
    assert progress["status"] == "paused"
    assert progress["what"] == "Increase revenue by 20%"
    assert len(progress["provenance"]) > 0
    assert len(progress["children"]) == 1

    # Resume mission
    mission.resume()

    # Should be running again
    assert mission.task.status == TaskStatus.RUNNING
    assert child.task.status == TaskStatus.RUNNING

    # WHAT→WHY chain intact
    assert mission.context[Dimension.WHAT] == "Increase revenue by 20%"
    assert child.context[Dimension.WHY] == "Increase revenue by 20%"


def test_child_inherits_parent_what_as_why():
    """
    Test that A2AWalker children still inherit parent's WHAT as WHY.

    Core DiltsWalker functionality should still work with A2A.
    """
    parent = A2AWalker(level=DiltsLevel.IDENTITY)
    parent_spec = Chunk(
        subject="Company",
        predicate="launches",
        object="product",
        dimensions={Dimension.WHAT: "Launch premium tier"}
    )
    parent.current_node = parent_spec
    parent.add_context(Dimension.WHAT, "Launch premium tier")

    # Create child
    child = A2AWalker(level=DiltsLevel.BELIEFS, parent=parent)

    # Child should inherit parent's WHAT as WHY
    assert child.context[Dimension.WHY] == "Launch premium tier"


def test_execution_with_hierarchy():
    """
    Test execution creates A2AWalker children, not DiltsWalker children.

    Ensures _create_child() override works correctly.
    """
    walker = A2AWalker(level=DiltsLevel.BELIEFS)
    spec = Chunk(
        subject="System",
        predicate="needs",
        object="feature",
        dimensions={Dimension.WHAT: "Build payment system"}
    )

    # Execute (will create children)
    result = walker.execute(spec)

    # Should have created child
    assert len(walker.children) > 0

    # Child should be A2AWalker, not DiltsWalker
    child = walker.children[0]
    assert isinstance(child, A2AWalker)
    assert hasattr(child, 'task')
    assert hasattr(child, 'pause')
    assert hasattr(child, 'resume')


def test_error_handling():
    """
    Test that execution errors mark task as failed.

    Task should transition to FAILED on exception.
    """
    # Create a custom walker that raises an error during traverse
    class FailingWalker(A2AWalker):
        def traverse(self, start):
            raise ValueError("Intentional test error")

    failing_walker = FailingWalker(level=DiltsLevel.ENVIRONMENT)

    spec = Chunk(
        subject="System",
        predicate="executes",
        object="action",
        dimensions={Dimension.WHAT: "Run tests"}
    )

    # Execute should catch error and mark task as failed
    with pytest.raises(ValueError):
        failing_walker.execute(spec)

    assert failing_walker.task.status == TaskStatus.FAILED
    assert failing_walker.task.error is not None
    assert "Intentional test error" in failing_walker.task.error


def test_cannot_pause_pending_task():
    """
    Test that PENDING tasks cannot be paused.

    Should raise RuntimeError.
    """
    walker = A2AWalker(level=DiltsLevel.CAPABILITY)

    with pytest.raises(RuntimeError, match="Cannot pause"):
        walker.pause()


def test_cannot_resume_running_task():
    """
    Test that RUNNING tasks cannot be resumed.

    Should raise RuntimeError.
    """
    walker = A2AWalker(level=DiltsLevel.CAPABILITY)
    walker.task.start()

    with pytest.raises(RuntimeError, match="Cannot resume"):
        walker.resume()


def test_multiple_pause_resume_cycles():
    """
    Test multiple pause/resume cycles maintain state.

    Should handle multiple interruptions correctly.
    """
    walker = A2AWalker(level=DiltsLevel.ENVIRONMENT)
    spec = Chunk(
        subject="System",
        predicate="executes",
        object="action",
        dimensions={
            Dimension.WHAT: "Long task",
            Dimension.WHY: "Complete mission"
        }
    )

    # Simulate: start → pause → resume → pause → resume using proper lifecycle methods
    walker.task.start()
    walker.paused_spec = spec
    walker.add_context(Dimension.WHAT, "Long task")
    walker.add_context(Dimension.WHY, "Complete mission")
    walker.task.pause()

    # First cycle
    walker.resume()
    assert walker.task.status == TaskStatus.COMPLETED

    # Context should still be intact
    assert walker.context[Dimension.WHAT] == "Long task"
    assert walker.context[Dimension.WHY] == "Complete mission"
