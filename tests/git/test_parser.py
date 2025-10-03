"""Tests for CommitMessageParser."""

import pytest
from pathlib import Path

from sixspec.core import CommitChunk, Dimension
from sixspec.git.parser import CommitMessageParser


class TestCommitMessageParser:
    """Test commit message parsing."""

    def test_parse_valid_commit_minimal(self):
        """Test parsing a commit with only required dimensions."""
        msg = """fix: payment timeout

WHY: Users abandoning carts at 25% rate
HOW: Added retry logic with exponential backoff"""

        commit = CommitMessageParser.parse(msg, "abc123")

        assert commit.subject == "fix"
        assert commit.object == "payment timeout"
        assert commit.predicate == "changes"
        assert commit.need(Dimension.WHY) == "Users abandoning carts at 25% rate"
        assert commit.need(Dimension.HOW) == "Added retry logic with exponential backoff"
        assert commit.commit_hash == "abc123"
        assert commit.commit_type == "fix"

    def test_parse_valid_commit_full(self):
        """Test parsing a commit with all dimensions."""
        msg = """fix: payment API timeout

WHY: Users abandoning carts at 25% rate due to timeout
HOW: Added retry logic with exponential backoff (3 attempts)
WHAT: Payment intent creation flow
WHERE: src/payment/stripe_integration.py"""

        commit = CommitMessageParser.parse(msg, "abc123")

        assert commit.subject == "fix"
        assert commit.object == "payment API timeout"
        assert commit.need(Dimension.WHY) == "Users abandoning carts at 25% rate due to timeout"
        assert commit.need(Dimension.HOW) == "Added retry logic with exponential backoff (3 attempts)"
        assert commit.need(Dimension.WHAT) == "Payment intent creation flow"
        assert commit.need(Dimension.WHERE) == "src/payment/stripe_integration.py"

    def test_parse_feat_commit(self):
        """Test parsing a feature commit."""
        msg = """feat: add search filters

WHY: Users cannot find products efficiently
HOW: Implemented faceted search with Elasticsearch
WHAT: Product search endpoint
WHERE: src/search/api.py
WHO: All users"""

        commit = CommitMessageParser.parse(msg, "def456")

        assert commit.commit_type == "feat"
        assert commit.object == "add search filters"
        assert commit.need(Dimension.WHO) == "All users"

    def test_parse_missing_why(self):
        """Test that parsing fails when WHY is missing."""
        msg = """fix: payment timeout

HOW: Added retry logic"""

        with pytest.raises(ValueError, match="Missing required dimension: WHY"):
            CommitMessageParser.parse(msg, "abc123")

    def test_parse_missing_how(self):
        """Test that parsing fails when HOW is missing."""
        msg = """fix: payment timeout

WHY: Users abandoning carts"""

        with pytest.raises(ValueError, match="Missing required dimension: HOW"):
            CommitMessageParser.parse(msg, "abc123")

    def test_parse_invalid_subject(self):
        """Test that parsing fails with invalid subject line."""
        msg = """invalid subject

WHY: Some reason
HOW: Some approach"""

        with pytest.raises(ValueError, match="Invalid subject line format"):
            CommitMessageParser.parse(msg, "abc123")

    def test_parse_empty_message(self):
        """Test that parsing fails with empty message."""
        with pytest.raises(ValueError, match="Empty commit message"):
            CommitMessageParser.parse("", "abc123")

    def test_parse_with_comments(self):
        """Test that comment lines are ignored."""
        msg = """fix: payment timeout
# This is a comment
WHY: Users abandoning carts
# Another comment
HOW: Added retry logic"""

        commit = CommitMessageParser.parse(msg, "abc123")
        assert commit.need(Dimension.WHY) == "Users abandoning carts"

    def test_parse_refactor_commit(self):
        """Test parsing a refactor commit."""
        msg = """refactor: extract payment validation

WHY: Code duplication across payment methods
HOW: Created shared validation module
WHERE: src/payment/validation.py, src/payment/stripe.py"""

        commit = CommitMessageParser.parse(msg, "ghi789")

        assert commit.commit_type == "refactor"
        assert commit.object == "extract payment validation"
        assert "duplication" in commit.need(Dimension.WHY)

    def test_has_and_need_methods(self):
        """Test has() and need() methods on parsed commit."""
        msg = """fix: payment timeout

WHY: Users abandoning carts
HOW: Added retry logic
WHERE: src/payment/stripe.py"""

        commit = CommitMessageParser.parse(msg, "abc123")

        assert commit.has(Dimension.WHY)
        assert commit.has(Dimension.HOW)
        assert commit.has(Dimension.WHERE)
        assert not commit.has(Dimension.WHO)

        assert commit.need(Dimension.WHERE) == "src/payment/stripe.py"
        assert commit.need(Dimension.WHO) is None

    def test_commit_w5h1_validation(self):
        """Test that CommitChunk validates required dimensions."""
        from sixspec.core import CommitChunk

        # Incomplete without WHY
        commit1 = CommitChunk(
            subject="fix",
            predicate="changes",
            object="something",
            dimensions={Dimension.HOW: "some approach"}
        )
        assert not commit1.is_complete()
        assert Dimension.WHY in commit1.required_dimensions()

        # Incomplete without HOW
        commit2 = CommitChunk(
            subject="fix",
            predicate="changes",
            object="something",
            dimensions={Dimension.WHY: "some reason"}
        )
        assert not commit2.is_complete()
        assert Dimension.HOW in commit2.required_dimensions()

        # Complete with both WHY and HOW
        commit3 = CommitChunk(
            subject="fix",
            predicate="changes",
            object="something",
            dimensions={
                Dimension.WHY: "some reason",
                Dimension.HOW: "some approach"
            }
        )
        assert commit3.has(Dimension.WHY)
        assert commit3.has(Dimension.HOW)
        assert commit3.is_complete()