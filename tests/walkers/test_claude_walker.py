"""
Tests for ClaudeWalker with Claude Agent SDK integration.

This test suite verifies the ClaudeWalker implementation including:
- Session management for pause/resume
- Subagent configuration
- WHAT→WHY propagation
- Progress tracking
- Context preservation

Note: These tests mock the Claude Agent SDK to avoid requiring
actual API keys and network access during testing.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sixspec.core.models import Dimension, DiltsLevel, Chunk
from sixspec.walkers.claude_walker import ClaudeWalker


@pytest.fixture
def mock_sdk_client():
    """Mock ClaudeSDKClient for testing."""
    with patch('sixspec.walkers.claude_walker.ClaudeSDKClient') as mock_client_class:
        # Mock the async context manager
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client_class.return_value = mock_client

        # Mock receive_response to yield messages
        async def mock_receive_response():
            # Yield init message with session ID
            init_msg = MagicMock()
            init_msg.subtype = 'init'
            init_msg.data = {'session_id': 'test-session-123'}
            yield init_msg

            # Yield result message
            result_msg = MagicMock()
            result_msg.result = "Test execution completed"
            yield result_msg

        mock_client.receive_response = mock_receive_response

        yield mock_client_class


@pytest.fixture
def mock_sdk_available():
    """Mock SDK availability."""
    with patch('sixspec.walkers.claude_walker.SDK_AVAILABLE', True):
        with patch('sixspec.walkers.claude_walker.ClaudeAgentOptions') as mock_options:
            # Mock ClaudeAgentOptions to return a proper object
            mock_options.return_value = MagicMock()
            yield


class TestClaudeWalkerBasics:
    """Test basic ClaudeWalker functionality."""

    def test_walker_initialization(self, mock_sdk_available):
        """Test ClaudeWalker initialization."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)

        assert walker.level == DiltsLevel.CAPABILITY
        assert walker.session_id is None
        assert walker.is_paused is False
        assert walker.client is None
        assert walker.paused_spec is None
        assert walker.execution_result is None

    def test_parent_child_relationship(self, mock_sdk_available):
        """Test parent-child walker creation."""
        parent = ClaudeWalker(level=DiltsLevel.IDENTITY)
        parent.add_context(Dimension.WHAT, "Build product")
        parent.current_node = Chunk(
            subject="Company",
            predicate="builds",
            object="product",
            dimensions={Dimension.WHAT: "Build product"}
        )

        child = ClaudeWalker(level=DiltsLevel.BELIEFS, parent=parent)

        assert child.parent == parent
        assert child.context.get(Dimension.WHY) == "Build product"

    def test_create_child(self, mock_sdk_available):
        """Test _create_child creates ClaudeWalker instances."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        child = parent._create_child(DiltsLevel.BEHAVIOR)

        assert isinstance(child, ClaudeWalker)
        assert child.level == DiltsLevel.BEHAVIOR
        assert child.parent == parent


class TestClaudeWalkerExecution:
    """Test ClaudeWalker execution with mocked SDK."""

    @pytest.mark.asyncio
    async def test_execute_basic(self, mock_sdk_available, mock_sdk_client):
        """Test basic execution flow."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        spec = Chunk(
            subject="System",
            predicate="needs",
            object="feature",
            dimensions={Dimension.WHAT: "Integrate payment"}
        )

        result = await walker.execute(spec)

        assert result == "Test execution completed"
        assert walker.session_id == 'test-session-123'
        assert walker.execution_result is not None

    @pytest.mark.asyncio
    async def test_execute_with_parent_context(self, mock_sdk_available, mock_sdk_client):
        """Test execution preserves parent's WHAT as WHY."""
        parent = ClaudeWalker(level=DiltsLevel.IDENTITY)
        parent.add_context(Dimension.WHAT, "Launch product")
        parent.current_node = Chunk(
            subject="Company",
            predicate="launches",
            object="product",
            dimensions={Dimension.WHAT: "Launch product"}
        )

        child = ClaudeWalker(level=DiltsLevel.BELIEFS, parent=parent)
        spec = Chunk(
            subject="Team",
            predicate="chooses",
            object="strategy",
            dimensions={Dimension.WHAT: "Define go-to-market"}
        )

        await child.execute(spec)

        assert child.context.get(Dimension.WHY) == "Launch product"
        assert child.context.get(Dimension.WHAT) == "Define go-to-market"


class TestClaudeWalkerPauseResume:
    """Test pause/resume functionality."""

    @pytest.mark.asyncio
    async def test_pause(self, mock_sdk_available):
        """Test pausing walker."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        walker.session_id = 'test-session-456'

        # Mock client
        mock_client = AsyncMock()
        walker.client = mock_client

        session_id = await walker.pause()

        assert walker.is_paused is True
        assert session_id == 'test-session-456'
        mock_client.interrupt.assert_called_once()

    @pytest.mark.asyncio
    async def test_pause_cascades_to_children(self, mock_sdk_available):
        """Test pause cascades to child walkers."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        child1 = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        child2 = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)

        parent.children = [child1, child2]
        parent.session_id = 'parent-session'
        child1.session_id = 'child1-session'
        child2.session_id = 'child2-session'

        # Mock clients
        parent.client = AsyncMock()
        child1.client = AsyncMock()
        child2.client = AsyncMock()

        await parent.pause()

        assert parent.is_paused is True
        assert child1.is_paused is True
        assert child2.is_paused is True

    @pytest.mark.asyncio
    async def test_resume(self, mock_sdk_available, mock_sdk_client):
        """Test resuming from paused state."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        spec = Chunk(
            subject="System",
            predicate="needs",
            object="feature",
            dimensions={Dimension.WHAT: "Integrate payment"}
        )

        result = await walker.resume('previous-session-123', spec)

        assert result == "Test execution completed"
        assert walker.is_paused is False


class TestClaudeWalkerConfiguration:
    """Test configuration building for SDK."""

    def test_build_subagent_config_no_children(self, mock_sdk_available):
        """Test subagent config with no children."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        config = walker._build_subagent_config()

        assert config is None

    def test_build_subagent_config_with_children(self, mock_sdk_available):
        """Test subagent config with children."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        child = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        parent.children = [child]

        config = parent._build_subagent_config()

        assert config is not None
        assert 'dilts_level_2' in config
        assert config['dilts_level_2']['description'].startswith('Handle BEHAVIOR')
        assert 'prompt' in config['dilts_level_2']
        assert 'tools' in config['dilts_level_2']
        assert 'model' in config['dilts_level_2']

    def test_build_system_prompt(self, mock_sdk_available):
        """Test system prompt building."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        walker.add_context(Dimension.WHY, "Launch product")
        spec = Chunk(
            subject="System",
            predicate="needs",
            object="feature",
            dimensions={Dimension.WHAT: "Integrate payment"}
        )

        prompt = walker._build_system_prompt(spec)

        assert "Dilts Level 3 (CAPABILITY)" in prompt
        assert "Integrate payment" in prompt
        assert "Launch product" in prompt
        assert "WHAT→WHY" in prompt

    def test_build_prompt(self, mock_sdk_available):
        """Test execution prompt building."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        spec = Chunk(
            subject="System",
            predicate="needs",
            object="feature",
            dimensions={Dimension.WHAT: "Integrate payment"}
        )

        prompt = walker._build_prompt(spec)

        assert "Execute: Integrate payment" in prompt

    def test_build_child_system_prompt(self, mock_sdk_available):
        """Test child system prompt building."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        child = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        child.add_context(Dimension.WHY, "Integrate payment")

        prompt = parent._build_child_system_prompt(child)

        assert "BEHAVIOR level agent" in prompt
        assert "Integrate payment" in prompt
        assert "WHY:" in prompt


class TestClaudeWalkerProgress:
    """Test progress tracking."""

    def test_get_progress_basic(self, mock_sdk_available):
        """Test basic progress retrieval."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        walker.add_context(Dimension.WHAT, "Build feature")
        walker.add_context(Dimension.WHY, "Launch product")
        walker.session_id = 'test-session-789'

        progress = walker.get_progress()

        assert progress['level'] == 3
        assert progress['session_id'] == 'test-session-789'
        assert progress['is_paused'] is False
        assert progress['what'] == "Build feature"
        assert progress['why'] == "Launch product"
        assert 'children' in progress

    def test_get_progress_with_children(self, mock_sdk_available):
        """Test progress includes children."""
        parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        child = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
        parent.children = [child]

        parent.add_context(Dimension.WHAT, "Build feature")
        child.add_context(Dimension.WHAT, "Write code")

        progress = parent.get_progress()

        assert len(progress['children']) == 1
        assert progress['children'][0]['level'] == 2
        assert progress['children'][0]['what'] == "Write code"

    def test_update_what(self, mock_sdk_available):
        """Test updating WHAT while preserving WHY."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        walker.add_context(Dimension.WHAT, "Use Stripe")
        walker.add_context(Dimension.WHY, "Process payments")

        walker.update_what("Use PayPal")

        assert walker.context[Dimension.WHAT] == "Use PayPal"
        assert walker.context[Dimension.WHY] == "Process payments"


class TestClaudeWalkerProvenance:
    """Test provenance tracing."""

    def test_trace_provenance_single_level(self, mock_sdk_available):
        """Test provenance with single level."""
        walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
        walker.add_context(Dimension.WHAT, "Build feature")

        chain = walker.trace_provenance()

        assert chain == ["Build feature"]

    def test_trace_provenance_multi_level(self, mock_sdk_available):
        """Test provenance with multiple levels."""
        L6 = ClaudeWalker(level=DiltsLevel.MISSION)
        L6.add_context(Dimension.WHAT, "Dominate market")

        L5 = ClaudeWalker(level=DiltsLevel.IDENTITY, parent=L6)
        L5.add_context(Dimension.WHAT, "Be best product")

        L4 = ClaudeWalker(level=DiltsLevel.BELIEFS, parent=L5)
        L4.add_context(Dimension.WHAT, "Focus on quality")

        chain = L4.trace_provenance()

        assert chain == ["Dominate market", "Be best product", "Focus on quality"]


class TestClaudeWalkerErrorHandling:
    """Test error handling."""

    def test_sdk_not_available(self):
        """Test error when SDK not installed."""
        with patch('sixspec.walkers.claude_walker.SDK_AVAILABLE', False):
            with pytest.raises(ImportError, match="claude-agent-sdk is required"):
                ClaudeWalker(level=DiltsLevel.CAPABILITY)

    @pytest.mark.asyncio
    async def test_execute_failure(self, mock_sdk_available):
        """Test execution failure handling."""
        with patch('sixspec.walkers.claude_walker.ClaudeSDKClient') as mock_client_class:
            # Mock client that raises an error
            mock_client = AsyncMock()
            mock_client.__aenter__.side_effect = Exception("Connection failed")
            mock_client_class.return_value = mock_client

            walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
            spec = Chunk(
                subject="System",
                predicate="needs",
                object="feature",
                dimensions={Dimension.WHAT: "Integrate payment"}
            )

            with pytest.raises(RuntimeError, match="ClaudeWalker execution failed"):
                await walker.execute(spec)
