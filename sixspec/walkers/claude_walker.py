"""
ClaudeWalker: DiltsWalker enhanced with Claude Agent SDK integration.

This module extends DiltsWalker with the Claude Agent SDK for graceful
interruption, pause/resume via session management, and hierarchical task
coordination using subagents.

Key Features:
- Graceful pause at any Dilts level using SDK interrupt
- Resume from exact position using session IDs
- WHAT→WHY chain preserved during pause/resume
- Cascade pause propagates to all children via subagents
- Real-time progress tracking via message streaming
- Progress inspection with full provenance

Example:
    >>> from sixspec.walkers.claude_walker import ClaudeWalker
    >>> from sixspec.core.models import DiltsLevel, Chunk, Dimension
    >>> import asyncio
    >>>
    >>> async def main():
    ...     # Create and execute walker
    ...     walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
    ...     spec = Chunk(
    ...         subject="System",
    ...         predicate="needs",
    ...         object="payment",
    ...         dimensions={Dimension.WHAT: "Integrate payment"}
    ...     )
    ...     await walker.execute(spec)
    ...
    ...     # Pause mid-execution
    ...     await walker.pause()
    ...
    ...     # Inspect progress
    ...     progress = walker.get_progress()
    ...
    ...     # Resume later
    ...     session_id = walker.session_id
    ...     await walker.resume(session_id, spec)
    >>>
    >>> asyncio.run(main())
"""

import asyncio
from typing import Any, Dict, List, Optional

from sixspec.core.models import Dimension, DiltsLevel, Chunk
from sixspec.walkers.dilts_walker import DiltsWalker

try:
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    ClaudeSDKClient = None
    ClaudeAgentOptions = None


class ClaudeWalker(DiltsWalker):
    """
    DiltsWalker enhanced with Claude Agent SDK integration.

    Extends DiltsWalker with Claude Agent SDK capabilities:
    - Session management for pause/resume
    - Subagent coordination for child walkers
    - Real-time message streaming for progress tracking
    - Interrupt support for graceful pause
    - Full WHAT→WHY chain preservation

    Attributes:
        session_id: Claude SDK session ID for resumption
        is_paused: Whether walker is currently paused
        client: ClaudeSDKClient instance (created during execution)
        paused_spec: Spec saved during pause for resume
        execution_result: Result saved for completion

    Example:
        >>> async def example():
        ...     walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        ...     spec = Chunk("A", "B", "C", dimensions={
        ...         Dimension.WHAT: "Build feature"
        ...     })
        ...     result = await walker.execute(spec)
        ...     print(f"Session: {walker.session_id}")
        >>> asyncio.run(example())
    """

    def __init__(self, level: DiltsLevel, parent: Optional['ClaudeWalker'] = None):
        """
        Initialize a ClaudeWalker.

        Creates session tracking and inherits parent's WHAT as WHY (like DiltsWalker).
        If parent exists, will be configured as a subagent in the SDK.

        Args:
            level: Dilts level this walker operates at
            parent: Optional parent walker (one level higher)

        Raises:
            ImportError: If claude-agent-sdk is not installed

        Example:
            >>> parent = ClaudeWalker(level=DiltsLevel.IDENTITY)
            >>> child = ClaudeWalker(level=DiltsLevel.BELIEFS, parent=parent)
            >>> child.context.get(Dimension.WHY) == parent.context.get(Dimension.WHAT)
            True
        """
        if not SDK_AVAILABLE:
            raise ImportError(
                "claude-agent-sdk is required for ClaudeWalker. "
                "Install it with: pip install claude-agent-sdk"
            )

        super().__init__(level, parent)

        # Session tracking instead of Task lifecycle
        self.session_id: Optional[str] = None
        self.is_paused: bool = False

        # SDK client (created during execution)
        self.client: Optional[ClaudeSDKClient] = None

        # State for pause/resume
        self.paused_spec: Optional[Chunk] = None
        self.execution_result: Optional[Any] = None

    def _create_child(self, child_level: DiltsLevel) -> 'ClaudeWalker':
        """
        Create a ClaudeWalker child (not plain DiltsWalker).

        Overrides DiltsWalker._create_child to ensure we create
        ClaudeWalker children that support pause/resume.

        Args:
            child_level: Dilts level for child

        Returns:
            New ClaudeWalker instance
        """
        return ClaudeWalker(level=child_level, parent=self)

    async def execute(self, spec: Chunk) -> Any:
        """
        Execute with Claude Agent SDK session management.

        Wraps normal DiltsWalker execution with SDK session lifecycle:
        - Configure subagents based on Dilts children
        - Build system prompt with WHAT→WHY context
        - Create SDK client and connect
        - Execute via Claude with tool access
        - Capture session ID for resumption
        - Support resume from paused state

        Args:
            spec: Chunk specification to execute

        Returns:
            Result from execution

        Raises:
            RuntimeError: If SDK client fails to connect

        Example:
            >>> async def example():
            ...     walker = ClaudeWalker(level=DiltsLevel.ENVIRONMENT)
            ...     spec = Chunk("A", "B", "C", dimensions={
            ...         Dimension.WHAT: "Run tests"
            ...     })
            ...     result = await walker.execute(spec)
            ...     return result
            >>> asyncio.run(example())
        """
        # Set current node and context
        self.current_node = spec
        my_what = spec.need(Dimension.WHAT)
        if my_what:
            self.add_context(Dimension.WHAT, my_what)

        # Configure SDK options with subagents
        agents_config = self._build_subagent_config()

        options = ClaudeAgentOptions(
            agents=agents_config if agents_config else None,
            allowed_tools=["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
            system_prompt=self._build_system_prompt(spec)
        )

        # Create and connect client
        try:
            async with ClaudeSDKClient(options=options) as client:
                self.client = client

                # Build prompt with dimensional context
                prompt = self._build_prompt(spec)
                await client.query(prompt)

                # Process responses and capture session ID
                result = await self._process_responses(client)

                self.execution_result = result
                return result

        except Exception as e:
            raise RuntimeError(f"ClaudeWalker execution failed: {e}")

    async def pause(self) -> str:
        """
        Gracefully pause this walker and all children.

        Uses SDK interrupt to stop execution. Captures current state
        for later resumption. Preserves full WHAT→WHY chain and
        dimensional context.

        Returns:
            Session ID for resuming (can be None if not yet started)

        After pause:
        - is_paused == True
        - session_id available for resume
        - All children are paused (via cascade)
        - WHAT→WHY chain intact
        - Can inspect progress with get_progress()
        - Can resume() to continue from this point

        Example:
            >>> async def example():
            ...     walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
            ...     # Start execution in background
            ...     # ...
            ...     session_id = await walker.pause()
            ...     print(f"Paused at session: {session_id}")
            >>> asyncio.run(example())
        """
        if self.client and not self.is_paused:
            await self.client.interrupt()
            self.is_paused = True

        # Cascade pause to children
        for child in self.children:
            if isinstance(child, ClaudeWalker):
                await child.pause()

        return self.session_id

    async def resume(self, session_id: str, spec: Chunk) -> Any:
        """
        Resume execution from paused state using session ID.

        Uses SDK's resume option to continue from where we left off.
        Restores full WHAT→WHY chain and dimensional context.

        Args:
            session_id: Session ID from previous execution
            spec: Original spec (for context restoration)

        Returns:
            Result from continued execution

        Raises:
            RuntimeError: If resume fails

        Example:
            >>> async def example():
            ...     walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
            ...     spec = Chunk("A", "B", "C", dimensions={
            ...         Dimension.WHAT: "Build feature"
            ...     })
            ...     # Assume walker was paused during execution
            ...     session_id = "some-session-id"
            ...     result = await walker.resume(session_id, spec)
            ...     return result
            >>> asyncio.run(example())
        """
        # Configure options with resume
        agents_config = self._build_subagent_config()

        options = ClaudeAgentOptions(
            resume=session_id,
            agents=agents_config if agents_config else None,
            allowed_tools=["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
            system_prompt=self._build_system_prompt(spec)
        )

        try:
            async with ClaudeSDKClient(options=options) as client:
                self.client = client

                # Continue with new prompt
                prompt = f"Continue from where we left off: {self._build_prompt(spec)}"
                await client.query(prompt)

                # Process responses
                result = await self._process_responses(client)

                self.is_paused = False
                self.execution_result = result
                return result

        except Exception as e:
            raise RuntimeError(f"ClaudeWalker resume failed: {e}")

    def _build_subagent_config(self) -> Optional[Dict[str, Any]]:
        """
        Build subagent configuration from Dilts children.

        Each child walker becomes a subagent with:
        - Level-specific description
        - WHAT→WHY context in system prompt
        - Appropriate tool access
        - Model selection based on level

        Returns:
            Dictionary of subagent configurations, or None if no children
        """
        if not self.children:
            return None

        agents = {}
        for child in self.children:
            if isinstance(child, ClaudeWalker):
                agent_name = f"dilts_level_{child.level.value}"
                agents[agent_name] = {
                    'description': f'Handle {child.level.name} level tasks ({child.level.autonomy} autonomy)',
                    'prompt': self._build_child_system_prompt(child),
                    'tools': ['Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob'],
                    'model': 'sonnet'  # Can be customized per level
                }

        return agents

    def _build_system_prompt(self, spec: Chunk) -> str:
        """
        Build system prompt with WHAT→WHY context.

        Creates a system prompt that embeds:
        - Current Dilts level and autonomy
        - WHAT dimension (current action)
        - WHY dimension (inherited from parent)
        - Purpose propagation instructions

        Args:
            spec: Chunk specification for context

        Returns:
            System prompt string with dimensional context
        """
        what = spec.need(Dimension.WHAT) or "unspecified action"
        why = self.context.get(Dimension.WHY, "no parent context")

        prompt = f"""You are operating at Dilts Level {self.level.value} ({self.level.name}).

Autonomy Level: {self.level.autonomy}
Primary Dimensions: {', '.join(d.value for d in self.level.primary_dimensions)}

WHAT you need to do: {what}
WHY you're doing it: {why}

CRITICAL: Maintain the WHAT→WHY chain in all decisions and delegate to child levels when appropriate.
When you create sub-tasks, your current WHAT becomes their WHY.

This ensures full traceability and purpose propagation throughout the system."""

        return prompt

    def _build_prompt(self, spec: Chunk) -> str:
        """
        Build execution prompt from spec.

        Args:
            spec: Chunk specification

        Returns:
            Prompt string for Claude
        """
        what = spec.need(Dimension.WHAT) or "execute specification"
        return f"Execute: {what}"

    async def _process_responses(self, client: ClaudeSDKClient) -> Any:
        """
        Process responses from Claude SDK and extract result.

        Captures session ID from init message and extracts final result.

        Args:
            client: ClaudeSDKClient instance

        Returns:
            Execution result
        """
        result = None

        async for message in client.receive_response():
            # Capture session ID from init message
            if hasattr(message, 'subtype') and message.subtype == 'init':
                self.session_id = message.data.get('session_id')

            # Track result from final message
            if hasattr(message, 'result'):
                result = message.result

        return result

    def _build_child_system_prompt(self, child: 'ClaudeWalker') -> str:
        """
        Build system prompt for child subagent.

        Args:
            child: Child ClaudeWalker instance

        Returns:
            System prompt for child subagent
        """
        why = child.context.get(Dimension.WHY, "parent's WHAT not propagated")

        return f"""You are a {child.level.name} level agent.

Your parent's WHAT is your WHY.
WHY: {why}

Focus on {child.level.name}-level concerns and delegate further if needed.
Primary dimensions for your level: {', '.join(d.value for d in child.level.primary_dimensions)}
Autonomy: {child.level.autonomy}"""

    def get_progress(self) -> Dict[str, Any]:
        """
        Get current execution state for inspection.

        Returns full dimensional context including:
        - Current Dilts level
        - Session status (session_id, is_paused)
        - WHAT and WHY dimensions
        - Full provenance chain
        - Progress from all children

        This enables users to inspect walker state during pause
        or while running.

        Returns:
            Dictionary with complete execution state

        Example:
            >>> walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
            >>> progress = walker.get_progress()
            >>> progress['level']
            3
        """
        progress = {
            "walker_id": self.name,
            "level": self.level.value,
            "session_id": self.session_id,
            "is_paused": self.is_paused,
            "what": self.context.get(Dimension.WHAT),
            "why": self.context.get(Dimension.WHY),
            "provenance": self.trace_provenance(),
            "children": []
        }

        # Include progress from children
        for child in self.children:
            if isinstance(child, ClaudeWalker):
                progress["children"].append(child.get_progress())

        return progress

    def update_what(self, new_what: str) -> None:
        """
        Update WHAT dimension while preserving WHY.

        Allows dynamic re-planning during pause: change the approach
        (WHAT) while keeping the purpose (WHY) intact.

        Args:
            new_what: New WHAT dimension value

        Example:
            >>> walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
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
