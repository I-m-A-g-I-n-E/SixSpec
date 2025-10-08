"""
Integration tests for ClaudeWalker implementation.

These tests verify the key features and patterns of ClaudeWalker including:
- WHAT→WHY propagation through hierarchies
- Subagent coordination
- Session management and persistence
- Progress tracking and provenance
- Hierarchical pause/resume
- Context preservation
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sixspec.core.models import Dimension, DiltsLevel, Chunk
from sixspec.walkers.claude_walker import ClaudeWalker


@pytest.fixture
def mock_sdk_environment():
    """Mock the complete SDK environment for integration testing."""
    with patch('sixspec.walkers.claude_walker.SDK_AVAILABLE', True):
        with patch('sixspec.walkers.claude_walker.ClaudeAgentOptions') as mock_options:
            with patch('sixspec.walkers.claude_walker.ClaudeSDKClient') as mock_client_class:
                # Mock ClaudeAgentOptions
                mock_options.return_value = MagicMock()

                # Mock ClaudeSDKClient
                mock_client = AsyncMock()
                mock_client.__aenter__.return_value = mock_client
                mock_client.__aexit__.return_value = None
                mock_client_class.return_value = mock_client

                # Mock receive_response with session tracking
                async def mock_receive_response():
                    # Init message with session
                    init_msg = MagicMock()
                    init_msg.subtype = 'init'
                    init_msg.data = {'session_id': f'session-{id(mock_client)}'}
                    yield init_msg

                    # Result message
                    result_msg = MagicMock()
                    result_msg.result = "Execution successful"
                    yield result_msg

                mock_client.receive_response = mock_receive_response

                yield {
                    'options': mock_options,
                    'client_class': mock_client_class,
                    'client': mock_client
                }


class TestWhatWhyPropagation:
    """Test WHAT→WHY propagation through walker hierarchies."""

    @pytest.mark.asyncio
    async def test_parent_what_becomes_child_why(self, mock_sdk_environment):
        """Test that parent's WHAT becomes child's WHY."""
        # Create parent at IDENTITY level
        parent = ClaudeWalker(level=DiltsLevel.IDENTITY)
        parent_spec = Chunk(
            subject="Company",
            predicate="launches",
            object="product",
            dimensions={Dimension.WHAT: "Launch premium tier"}
        )

        # Set up parent context
        parent.current_node = parent_spec
        parent.add_context(Dimension.WHAT, "Launch premium tier")

        # Create child at BELIEFS level
        child = ClaudeWalker(level=DiltsLevel.BELIEFS, parent=parent)

        # Verify child inherited parent's WHAT as WHY
        assert child.context.get(Dimension.WHY) == "Launch premium tier"
        assert child.parent == parent

    @pytest.mark.asyncio
    async def test_multi_level_propagation(self, mock_sdk_environment):
        """Test WHAT→WHY propagation through multiple levels."""
        # Level 6: Mission
        L6 = ClaudeWalker(level=DiltsLevel.MISSION)
        L6.add_context(Dimension.WHAT, "Dominate market")
        L6.current_node = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Dominate market"
        })

        # Level 5: Identity
        L5 = ClaudeWalker(level=DiltsLevel.IDENTITY, parent=L6)
        assert L5.context.get(Dimension.WHY) == "Dominate market"
        L5.add_context(Dimension.WHAT, "Be best product")
        L5.current_node = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Be best product"
        })

        # Level 4: Beliefs
        L4 = ClaudeWalker(level=DiltsLevel.BELIEFS, parent=L5)
        assert L4.context.get(Dimension.WHY) == "Be best product"
        L4.add_context(Dimension.WHAT, "Focus on quality")
        L4.current_node = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Focus on quality"
        })

        # Level 3: Capability
        L3 = ClaudeWalker(level=DiltsLevel.CAPABILITY, parent=L4)
        assert L3.context.get(Dimension.WHY) == "Focus on quality"

        # Trace full provenance
        L3.add_context(Dimension.WHAT, "Build testing framework")
        chain = L3.trace_provenance()

        assert chain == [
            "Dominate market",
            "Be best product",
            "Focus on quality",
            "Build testing framework"
        ]

    @pytest.mark.asyncio
    async def test_propagation_preserved_through_execution(self, mock_sdk_environment):
        """Test that WHAT→WHY chain is preserved during execution."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        parent.add_context(Dimension.WHAT, "Process payments")
        parent.current_node = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Process payments"
        })

        child = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        spec = Chunk(
            subject="System",
            predicate="integrates",
            object="Stripe",
            dimensions={Dimension.WHAT: "Integrate Stripe API"}
        )

        # Execute
        await child.execute(spec)

        # Verify WHY preserved
        assert child.context.get(Dimension.WHY) == "Process payments"
        assert child.context.get(Dimension.WHAT) == "Integrate Stripe API"


class TestSubagentConfiguration:
    """Test subagent coordination and configuration."""

    @pytest.mark.asyncio
    async def test_subagent_config_generation(self, mock_sdk_environment):
        """Test that subagent configuration is generated correctly."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)

        child1 = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        child1.add_context(Dimension.WHY, "Process payments")

        child2 = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        child2.add_context(Dimension.WHY, "Handle errors")

        parent.children = [child1, child2]

        config = parent._build_subagent_config()

        assert config is not None
        assert 'dilts_level_2' in config
        assert 'description' in config['dilts_level_2']
        assert 'prompt' in config['dilts_level_2']
        assert 'tools' in config['dilts_level_2']
        assert 'model' in config['dilts_level_2']

    @pytest.mark.asyncio
    async def test_subagent_system_prompts_include_why(self, mock_sdk_environment):
        """Test that subagent prompts include WHY dimension."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        parent.add_context(Dimension.WHAT, "Build auth system")
        parent.current_node = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Build auth system"
        })

        child = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)

        prompt = parent._build_child_system_prompt(child)

        assert "Build auth system" in prompt
        assert "WHY:" in prompt
        assert "BEHAVIOR" in prompt

    @pytest.mark.asyncio
    async def test_no_subagents_without_children(self, mock_sdk_environment):
        """Test that subagent config is None when there are no children."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        config = walker._build_subagent_config()
        assert config is None


class TestSessionManagement:
    """Test session persistence and recovery."""

    @pytest.mark.asyncio
    async def test_session_id_captured_on_execute(self, mock_sdk_environment):
        """Test that session ID is captured during execution."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        spec = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Execute task"
        })

        await walker.execute(spec)

        assert walker.session_id is not None
        assert walker.session_id.startswith('session-')

    @pytest.mark.asyncio
    async def test_session_preserved_through_pause(self, mock_sdk_environment):
        """Test that session ID is preserved when pausing."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        spec = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Long running task"
        })

        await walker.execute(spec)
        original_session = walker.session_id

        # Mock client for pause
        walker.client = AsyncMock()
        session_id = await walker.pause()

        assert session_id == original_session
        assert walker.is_paused is True

    @pytest.mark.asyncio
    async def test_resume_uses_session_id(self, mock_sdk_environment):
        """Test that resume uses the provided session ID."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        spec = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Resumable task"
        })

        session_id = "previous-session-123"

        result = await walker.resume(session_id, spec)

        # Verify ClaudeAgentOptions was called with resume parameter
        mock_options = mock_sdk_environment['options']
        assert any(
            call_args.kwargs.get('resume') == session_id
            for call_args in mock_options.call_args_list
        )


class TestProgressTracking:
    """Test progress tracking and provenance."""

    @pytest.mark.asyncio
    async def test_progress_includes_session_info(self, mock_sdk_environment):
        """Test that progress includes session information."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        walker.session_id = "test-session-456"
        walker.is_paused = False
        walker.add_context(Dimension.WHAT, "Current task")
        walker.add_context(Dimension.WHY, "Parent purpose")

        progress = walker.get_progress()

        assert progress['session_id'] == "test-session-456"
        assert progress['is_paused'] is False
        assert progress['what'] == "Current task"
        assert progress['why'] == "Parent purpose"
        assert progress['level'] == 3

    @pytest.mark.asyncio
    async def test_progress_includes_children(self, mock_sdk_environment):
        """Test that progress includes child walker information."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        parent.add_context(Dimension.WHAT, "Parent task")
        parent.session_id = "parent-session"

        child1 = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        child1.add_context(Dimension.WHAT, "Child 1 task")
        child1.session_id = "child1-session"

        child2 = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        child2.add_context(Dimension.WHAT, "Child 2 task")
        child2.session_id = "child2-session"

        parent.children = [child1, child2]

        progress = parent.get_progress()

        assert len(progress['children']) == 2
        assert progress['children'][0]['what'] == "Child 1 task"
        assert progress['children'][1]['what'] == "Child 2 task"
        assert progress['children'][0]['session_id'] == "child1-session"

    @pytest.mark.asyncio
    async def test_provenance_chain_complete(self, mock_sdk_environment):
        """Test that provenance chain is complete through hierarchy."""
        L6 = ClaudeWalker(level=DiltsLevel.MISSION)
        L6.add_context(Dimension.WHAT, "Mission goal")

        L5 = ClaudeWalker(level=DiltsLevel.IDENTITY, parent=L6)
        L5.add_context(Dimension.WHAT, "Identity goal")

        L4 = ClaudeWalker(level=DiltsLevel.BELIEFS, parent=L5)
        L4.add_context(Dimension.WHAT, "Beliefs goal")

        provenance = L4.trace_provenance()

        assert len(provenance) == 3
        assert provenance[0] == "Mission goal"
        assert provenance[1] == "Identity goal"
        assert provenance[2] == "Beliefs goal"


class TestHierarchicalPauseResume:
    """Test hierarchical pause/resume behavior."""

    @pytest.mark.asyncio
    async def test_pause_cascades_to_all_children(self, mock_sdk_environment):
        """Test that pause cascades to all child walkers."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        parent.session_id = "parent-123"

        child1 = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        child1.session_id = "child1-123"

        child2 = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        child2.session_id = "child2-123"

        grandchild = ClaudeWalker(level=DiltsLevel.ENVIRONMENT, parent=child1)
        grandchild.session_id = "grandchild-123"

        parent.children = [child1, child2]
        child1.children = [grandchild]

        # Mock clients
        parent.client = AsyncMock()
        child1.client = AsyncMock()
        child2.client = AsyncMock()
        grandchild.client = AsyncMock()

        # Pause parent
        await parent.pause()

        # Verify all are paused
        assert parent.is_paused is True
        assert child1.is_paused is True
        assert child2.is_paused is True
        assert grandchild.is_paused is True

    @pytest.mark.asyncio
    async def test_context_preserved_during_pause(self, mock_sdk_environment):
        """Test that WHAT→WHY context is preserved during pause."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        parent.add_context(Dimension.WHAT, "Parent work")
        parent.add_context(Dimension.WHY, "Root purpose")
        parent.current_node = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Parent work"
        })

        child = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        child.add_context(Dimension.WHAT, "Child work")

        parent.children = [child]
        parent.client = AsyncMock()
        child.client = AsyncMock()

        # Pause
        await parent.pause()

        # Verify context preserved
        assert parent.context.get(Dimension.WHAT) == "Parent work"
        assert parent.context.get(Dimension.WHY) == "Root purpose"
        assert child.context.get(Dimension.WHY) == "Parent work"
        assert child.context.get(Dimension.WHAT) == "Child work"


class TestContextPreservation:
    """Test context preservation through operations."""

    @pytest.mark.asyncio
    async def test_update_what_preserves_why(self, mock_sdk_environment):
        """Test that updating WHAT preserves WHY."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        walker.add_context(Dimension.WHAT, "Original approach")
        walker.add_context(Dimension.WHY, "Original purpose")

        walker.update_what("New approach")

        assert walker.context[Dimension.WHAT] == "New approach"
        assert walker.context[Dimension.WHY] == "Original purpose"

    @pytest.mark.asyncio
    async def test_execution_preserves_parent_context(self, mock_sdk_environment):
        """Test that execution preserves parent context."""
        parent = ClaudeWalker(level=DiltsLevel.IDENTITY)
        parent.add_context(Dimension.WHAT, "Build product")
        parent.add_context(Dimension.WHY, "Serve customers")
        parent.current_node = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Build product"
        })

        child = ClaudeWalker(level=DiltsLevel.BELIEFS, parent=parent)
        spec = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Choose technology"
        })

        await child.execute(spec)

        # Parent context unchanged
        assert parent.context[Dimension.WHAT] == "Build product"
        assert parent.context[Dimension.WHY] == "Serve customers"

        # Child has parent's WHAT as WHY
        assert child.context[Dimension.WHY] == "Build product"


class TestSystemPromptGeneration:
    """Test system prompt generation with dimensional context."""

    @pytest.mark.asyncio
    async def test_system_prompt_includes_dimensions(self, mock_sdk_environment):
        """Test that system prompts include dimensional context."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        walker.add_context(Dimension.WHY, "Enable payments")

        spec = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Integrate Stripe"
        })

        prompt = walker._build_system_prompt(spec)

        assert "Dilts Level 3" in prompt
        assert "CAPABILITY" in prompt
        assert "Integrate Stripe" in prompt
        assert "Enable payments" in prompt
        assert "WHAT→WHY" in prompt

    @pytest.mark.asyncio
    async def test_system_prompt_includes_autonomy_level(self, mock_sdk_environment):
        """Test that system prompts include autonomy information."""
        walker = ClaudeWalker(level=DiltsLevel.MISSION)
        spec = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Strategic goal"
        })

        prompt = walker._build_system_prompt(spec)

        assert "extreme" in prompt.lower()
        assert "MISSION" in prompt

    @pytest.mark.asyncio
    async def test_execution_prompt_built_from_spec(self, mock_sdk_environment):
        """Test that execution prompt is built from spec."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        spec = Chunk("A", "B", "C", dimensions={
            Dimension.WHAT: "Execute specific action"
        })

        prompt = walker._build_prompt(spec)

        assert "Execute specific action" in prompt


class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.mark.asyncio
    async def test_sdk_not_available_raises_error(self):
        """Test that missing SDK raises ImportError."""
        with patch('sixspec.walkers.claude_walker.SDK_AVAILABLE', False):
            with pytest.raises(ImportError, match="claude-agent-sdk is required"):
                ClaudeWalker(level=DiltsLevel.CAPABILITY)

    @pytest.mark.asyncio
    async def test_execution_failure_raises_runtime_error(self, mock_sdk_environment):
        """Test that execution failures raise RuntimeError."""
        with patch('sixspec.walkers.claude_walker.ClaudeSDKClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.side_effect = Exception("Connection failed")
            mock_client_class.return_value = mock_client

            walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
            spec = Chunk("A", "B", "C", dimensions={
                Dimension.WHAT: "Failing task"
            })

            with pytest.raises(RuntimeError, match="ClaudeWalker execution failed"):
                await walker.execute(spec)

    @pytest.mark.asyncio
    async def test_pause_without_client_handles_gracefully(self, mock_sdk_environment):
        """Test that pause without client doesn't crash."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        walker.session_id = "test-123"
        walker.client = None  # No client

        session_id = await walker.pause()

        assert session_id == "test-123"
        assert walker.is_paused is True


class TestChildWalkerCreation:
    """Test child walker creation and relationships."""

    @pytest.mark.asyncio
    async def test_create_child_returns_claude_walker(self, mock_sdk_environment):
        """Test that _create_child returns ClaudeWalker instances."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        child = parent._create_child(DiltsLevel.BEHAVIOR)

        assert isinstance(child, ClaudeWalker)
        assert child.level == DiltsLevel.BEHAVIOR
        assert child.parent == parent

    @pytest.mark.asyncio
    async def test_child_hierarchy_preserves_types(self, mock_sdk_environment):
        """Test that entire hierarchy uses ClaudeWalker."""
        L3 = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        L2 = L3._create_child(DiltsLevel.BEHAVIOR)
        L1 = L2._create_child(DiltsLevel.ENVIRONMENT)

        assert isinstance(L3, ClaudeWalker)
        assert isinstance(L2, ClaudeWalker)
        assert isinstance(L1, ClaudeWalker)
        assert L2.parent == L3
        assert L1.parent == L2
