"""Tests for git hook validation."""

import pytest
import sys
import subprocess
from pathlib import Path


# Import the validation function from the hook script
def load_hook_module():
    """Load the commit-msg hook as a module."""
    hook_path = Path(__file__).parent.parent.parent / "sixspec" / "git" / "hooks" / "commit-msg"

    # Read and execute the hook file to get its functions
    with open(hook_path) as f:
        code = f.read()

    # Create a namespace and execute the code
    namespace = {}
    exec(code, namespace)

    return namespace['validate_commit_message']


validate_commit_message = load_hook_module()


class TestCommitMessageValidation:
    """Test commit message validation logic."""

    def test_valid_minimal_commit(self):
        """Test validation of minimal valid commit."""
        msg = """fix: payment timeout

WHY: Users abandoning carts
HOW: Added retry logic"""

        is_valid, errors = validate_commit_message(msg)
        assert is_valid
        assert len(errors) == 0

    def test_valid_full_commit(self):
        """Test validation of commit with all dimensions."""
        msg = """fix: payment API timeout

WHY: Users abandoning carts at 25% rate due to timeout
HOW: Added retry logic with exponential backoff (3 attempts)
WHAT: Payment intent creation flow
WHERE: src/payment/stripe_integration.py"""

        is_valid, errors = validate_commit_message(msg)
        assert is_valid
        assert len(errors) == 0

    def test_missing_why(self):
        """Test that validation fails when WHY is missing."""
        msg = """fix: payment timeout

HOW: Added retry logic"""

        is_valid, errors = validate_commit_message(msg)
        assert not is_valid
        assert "Missing required dimension: WHY" in errors

    def test_missing_how(self):
        """Test that validation fails when HOW is missing."""
        msg = """fix: payment timeout

WHY: Users abandoning carts"""

        is_valid, errors = validate_commit_message(msg)
        assert not is_valid
        assert "Missing required dimension: HOW" in errors

    def test_missing_both_dimensions(self):
        """Test that validation fails when both WHY and HOW are missing."""
        msg = """fix: payment timeout"""

        is_valid, errors = validate_commit_message(msg)
        assert not is_valid
        assert len(errors) == 2
        assert "Missing required dimension: WHY" in errors
        assert "Missing required dimension: HOW" in errors

    def test_invalid_subject_type(self):
        """Test that validation fails with invalid commit type."""
        msg = """invalid: something

WHY: Some reason
HOW: Some approach"""

        is_valid, errors = validate_commit_message(msg)
        assert not is_valid
        assert any("type:" in e for e in errors)

    def test_missing_subject_type(self):
        """Test that validation fails without type prefix."""
        msg = """no type prefix

WHY: Some reason
HOW: Some approach"""

        is_valid, errors = validate_commit_message(msg)
        assert not is_valid
        assert any("type:" in e for e in errors)

    def test_all_valid_commit_types(self):
        """Test that all documented commit types are valid."""
        types = ['feat', 'fix', 'refactor', 'docs', 'test', 'chore']

        for commit_type in types:
            msg = f"""{commit_type}: something

WHY: Some reason
HOW: Some approach"""

            is_valid, errors = validate_commit_message(msg)
            assert is_valid, f"{commit_type} should be valid but got errors: {errors}"

    def test_comments_are_ignored(self):
        """Test that comment lines are ignored."""
        msg = """fix: payment timeout
# This is a comment
WHY: Users abandoning carts
# Another comment
HOW: Added retry logic"""

        is_valid, errors = validate_commit_message(msg)
        assert is_valid

    def test_empty_message(self):
        """Test that empty message is allowed (for --amend)."""
        msg = ""

        is_valid, errors = validate_commit_message(msg)
        assert is_valid

    def test_merge_commit_skipped(self):
        """Test that merge commits are skipped."""
        msg = """Merge branch 'feature' into main"""

        is_valid, errors = validate_commit_message(msg)
        assert is_valid

    def test_multiline_dimensions(self):
        """Test validation with multiline dimension values."""
        msg = """fix: payment timeout

WHY: Users abandoning carts at 25% rate
HOW: Added retry logic with exponential backoff"""

        is_valid, errors = validate_commit_message(msg)
        assert is_valid

    def test_dimension_with_colon_in_value(self):
        """Test dimension values containing colons."""
        msg = """fix: payment timeout

WHY: Users abandoning carts: 25% rate observed
HOW: Added retry logic: 3 attempts with backoff"""

        is_valid, errors = validate_commit_message(msg)
        assert is_valid

    def test_case_sensitive_dimensions(self):
        """Test that dimension names are case-sensitive (uppercase required)."""
        msg = """fix: payment timeout

why: Users abandoning carts
how: Added retry logic"""

        is_valid, errors = validate_commit_message(msg)
        # Should fail because dimensions must be uppercase
        assert not is_valid
        assert "Missing required dimension: WHY" in errors
        assert "Missing required dimension: HOW" in errors

    def test_multiple_errors(self):
        """Test that all errors are reported together."""
        msg = """invalid type here

WHAT: Just a what"""

        is_valid, errors = validate_commit_message(msg)
        assert not is_valid
        assert len(errors) == 3  # Invalid type, missing WHY, missing HOW