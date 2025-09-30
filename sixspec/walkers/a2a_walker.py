"""
A2AWalker: DiltsWalker enhanced with A2A task lifecycle management.

This module extends DiltsWalker with Google's A2A protocol for graceful
interruption, pause/resume, and hierarchical task coordination.

Key Features:
- Graceful pause at any Dilts level
- Resume from exact position with full context
- WHAT→WHY chain preserved during pause/resume
- Cascade pause propagates to all children
- Real-time status streaming
- Progress inspection with full provenance

Example:
    >>> from sixspec.walkers.a2a_walker import A2AWalker
    >>> from sixspec.core.models import DiltsLevel, W5H1, Dimension
    >>>
    >>> # Create and execute walker
    >>> walker = A2AWalker(level=DiltsLevel.CAPABILITY)
    >>> spec = W5H1(
    ...     subject="System",
    ...     predicate="needs",
    ...     object="payment",
    ...     dimensions={Dimension.WHAT: "Integrate payment"}
    ... )
    >>> walker.execute(spec)
    >>>
    >>> # Pause mid-execution
    >>> walker.pause()
    >>>
    >>> # Inspect progress
    >>> progress = walker.get_progress()
    >>>
    >>> # Resume later
    >>> walker.resume()
"""

from typing import Any, Dict, List, Optional

from sixspec.a2a import Task, TaskStatus, StatusUpdate
from sixspec.core.models import Dimension, DiltsLevel, W5H1
from sixspec.walkers.dilts_walker import DiltsWalker


class A2AWalker(DiltsWalker):
    """
    DiltsWalker enhanced with A2A task lifecycle management.

    Extends DiltsWalker with A2A protocol capabilities:
    - Task lifecycle states (pending, running, paused, completed, failed)
    - Graceful pause/resume without losing WHAT→WHY chain
    - Cascade operations to children
    - Real-time status streaming
    - Progress inspection with full dimensional context

    Attributes:
        task: A2A Task for lifecycle management
        paused_spec: Spec saved during pause for resume
        execution_result: Result saved for completion

    Example:
        >>> walker = A2AWalker(level=DiltsLevel.CAPABILITY)
        >>> spec = W5H1("A", "B", "C", dimensions={
        ...     Dimension.WHAT: "Build feature"
        ... })
        >>> walker.execute(spec)
        >>> walker.task.status
        <TaskStatus.COMPLETED: 'completed'>
    """

    def __init__(self, level: DiltsLevel, parent: Optional['A2AWalker'] = None):
        """
        Initialize an A2AWalker.

        Creates A2A Task and inherits parent's WHAT as WHY (like DiltsWalker).
        If parent exists, registers with parent's task for coordination.

        Args:
            level: Dilts level this walker operates at
            parent: Optional parent walker (one level higher)

        Example:
            >>> parent = A2AWalker(level=DiltsLevel.IDENTITY)
            >>> child = A2AWalker(level=DiltsLevel.BELIEFS, parent=parent)
            >>> child.task.parent == parent.task
            True
        """
        super().__init__(level, parent)

        # Create A2A task with parent coordination
        parent_task = parent.task if parent and hasattr(parent, 'task') else None
        self.task = Task(
            task_id=f"A2A-{self.name}",
            parent=parent_task
        )

        # State for pause/resume
        self.paused_spec: Optional[W5H1] = None
        self.execution_result: Optional[Any] = None

        # Register child status handler if we have a parent
        if parent and hasattr(parent, 'task'):
            self.task.on_status_change(parent.handle_child_status)

    def _create_child(self, child_level: DiltsLevel) -> 'A2AWalker':
        """
        Create an A2AWalker child (not plain DiltsWalker).

        Overrides DiltsWalker._create_child to ensure we create
        A2AWalker children that support pause/resume.

        Args:
            child_level: Dilts level for child

        Returns:
            New A2AWalker instance
        """
        return A2AWalker(level=child_level, parent=self)

    def execute(self, spec: W5H1) -> Any:
        """
        Execute with A2A task lifecycle tracking.

        Wraps normal DiltsWalker execution with task lifecycle:
        - Start task before execution
        - Track execution status
        - Complete task on success
        - Fail task on error
        - Support resume from paused state

        Args:
            spec: W5H1 specification to execute

        Returns:
            Result from execution

        Raises:
            InterruptedError: If execution was paused

        Example:
            >>> walker = A2AWalker(level=DiltsLevel.ENVIRONMENT)
            >>> spec = W5H1("A", "B", "C", dimensions={
            ...     Dimension.WHAT: "Run tests"
            ... })
            >>> result = walker.execute(spec)
            >>> walker.task.status
            <TaskStatus.COMPLETED: 'completed'>
        """
        # Start task if not already running
        if self.task.status == TaskStatus.PENDING:
            self.task.start()

        try:
            # Execute via parent's traverse method
            result = self.traverse(spec)

            # Complete task on success
            if self.task.status == TaskStatus.RUNNING:
                self.task.complete(result)

            self.execution_result = result
            return result

        except InterruptedError:
            # Graceful pause - save state and re-raise
            self.paused_spec = spec
            self.task.pause()
            raise

        except Exception as e:
            # Execution failed - mark task as failed
            self.task.fail(str(e))
            raise

    def pause(self) -> None:
        """
        Gracefully pause this walker and all children.

        Pauses task lifecycle and cascades to all child walkers.
        Preserves full WHAT→WHY chain and dimensional context.

        After pause:
        - task.status == PAUSED
        - All children are paused
        - WHAT→WHY chain intact
        - Can inspect progress with get_progress()
        - Can resume() to continue from this point

        Example:
            >>> walker = A2AWalker(level=DiltsLevel.CAPABILITY)
            >>> walker.task.start()
            >>> walker.pause()
            >>> walker.task.status
            <TaskStatus.PAUSED: 'paused'>
        """
        # Let Task handle the cascade to children
        self.task.pause()

    def resume(self) -> Optional[Any]:
        """
        Resume execution from paused state.

        Resumes task lifecycle and continues execution from where it
        paused. Restores full WHAT→WHY chain and dimensional context.

        Returns:
            Result from continued execution

        Raises:
            RuntimeError: If not in PAUSED state

        Example:
            >>> walker = A2AWalker(level=DiltsLevel.CAPABILITY)
            >>> spec = W5H1("A", "B", "C", dimensions={
            ...     Dimension.WHAT: "Build feature"
            ... })
            >>> # Assume walker was paused during execution
            >>> walker.task.status = TaskStatus.PAUSED
            >>> walker.paused_spec = spec
            >>> walker.resume()
        """
        if self.task.status != TaskStatus.PAUSED:
            raise RuntimeError(
                f"Cannot resume walker in {self.task.status.value} state"
            )

        # Resume task lifecycle (resumes children too)
        self.task.resume()

        # Continue execution from saved spec
        if self.paused_spec:
            return self.execute(self.paused_spec)

        return self.execution_result

    def handle_child_status(self, update: StatusUpdate) -> None:
        """
        Handle real-time status updates from child walkers.

        Called when child task changes status. Enables parent to:
        - React to child completion
        - Propagate child failures
        - Coordinate pause operations

        Args:
            update: StatusUpdate from child task

        Example:
            >>> parent = A2AWalker(level=DiltsLevel.IDENTITY)
            >>> child = A2AWalker(level=DiltsLevel.BELIEFS, parent=parent)
            >>> # Child status changes automatically notify parent
        """
        if update.status == TaskStatus.COMPLETED:
            self.on_child_complete(update)
        elif update.status == TaskStatus.FAILED:
            self.on_child_failure(update)
        elif update.status == TaskStatus.PAUSED:
            self.on_child_paused(update)

    def on_child_complete(self, update: StatusUpdate) -> None:
        """
        Handle child completion.

        Args:
            update: StatusUpdate with completion details
        """
        # Default: no action needed, child completed successfully
        pass

    def on_child_failure(self, update: StatusUpdate) -> None:
        """
        Handle child failure.

        Args:
            update: StatusUpdate with error details
        """
        # Default: could propagate failure up, but let parent decide
        pass

    def on_child_paused(self, update: StatusUpdate) -> None:
        """
        Handle child pause.

        Args:
            update: StatusUpdate with pause notification
        """
        # Default: no action needed, child paused independently
        pass

    def get_progress(self) -> Dict[str, Any]:
        """
        Get current execution state for inspection.

        Returns full dimensional context including:
        - Current Dilts level
        - Task status
        - WHAT and WHY dimensions
        - Full provenance chain
        - Progress from all children

        This enables users to inspect walker state during pause
        or while running.

        Returns:
            Dictionary with complete execution state

        Example:
            >>> walker = A2AWalker(level=DiltsLevel.CAPABILITY)
            >>> spec = W5H1("A", "B", "C", dimensions={
            ...     Dimension.WHAT: "Build feature",
            ...     Dimension.WHY: "Launch product"
            ... })
            >>> walker.execute(spec)
            >>> progress = walker.get_progress()
            >>> progress['level']
            3
            >>> progress['what']
            'Build feature'
        """
        progress = {
            "walker_id": self.name,
            "level": self.level.value,
            "status": self.task.status.value,
            "what": self.context.get(Dimension.WHAT),
            "why": self.context.get(Dimension.WHY),
            "provenance": self.trace_provenance(),
            "children": []
        }

        # Include progress from children
        for child in self.children:
            if isinstance(child, A2AWalker):
                progress["children"].append(child.get_progress())

        return progress

    def stream_status(self):
        """
        Stream status updates in real-time.

        Yields status updates while walker is executing. Useful for
        monitoring long-running operations via gRPC or similar protocols.

        Yields:
            Dictionary with current status and progress

        Example:
            >>> walker = A2AWalker(level=DiltsLevel.CAPABILITY)
            >>> walker.task.start()
            >>> for status in walker.stream_status():
            ...     print(f"Progress: {status['progress_pct']}%")
            ...     if status['status'] in ['completed', 'failed', 'paused']:
            ...         break
        """
        while not self.task.status.is_terminal():
            yield {
                "walker_id": self.name,
                "level": self.level.value,
                "status": self.task.status.value,
                "what": self.context.get(Dimension.WHAT),
                "progress_pct": self.calculate_progress()
            }

            if self.task.status == TaskStatus.PAUSED:
                break

    def calculate_progress(self) -> float:
        """
        Calculate progress percentage.

        Estimates progress based on:
        - Current task status
        - Children completion status
        - Dilts level depth

        Returns:
            Progress percentage (0.0-100.0)

        Example:
            >>> walker = A2AWalker(level=DiltsLevel.ENVIRONMENT)
            >>> walker.task.status = TaskStatus.COMPLETED
            >>> walker.calculate_progress()
            100.0
        """
        if self.task.status == TaskStatus.COMPLETED:
            return 100.0
        elif self.task.status == TaskStatus.FAILED:
            return 0.0
        elif not self.children:
            # No children yet, estimate based on status
            return 50.0 if self.task.status == TaskStatus.RUNNING else 0.0
        else:
            # Aggregate children progress
            if not self.children:
                return 0.0

            total = 0.0
            for child in self.children:
                if isinstance(child, A2AWalker):
                    total += child.calculate_progress()
                else:
                    # Regular DiltsWalker child, assume 50% if exists
                    total += 50.0

            return total / len(self.children)

    def update_what(self, new_what: str) -> None:
        """
        Update WHAT dimension while preserving WHY.

        Allows dynamic re-planning during pause: change the approach
        (WHAT) while keeping the purpose (WHY) intact.

        Args:
            new_what: New WHAT dimension value

        Example:
            >>> walker = A2AWalker(level=DiltsLevel.CAPABILITY)
            >>> walker.add_context(Dimension.WHAT, "Use Stripe")
            >>> walker.add_context(Dimension.WHY, "Process payments")
            >>> walker.update_what("Use PayPal")
            >>> walker.context[Dimension.WHAT]
            'Use PayPal'
            >>> walker.context[Dimension.WHY]
            'Process payments'
        """
        self.add_context(Dimension.WHAT, new_what)

        # Update current_node if it exists
        if self.current_node:
            self.current_node.set(Dimension.WHAT, new_what)
