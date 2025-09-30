"""Tests for DimensionalGitHistory."""

import pytest
import tempfile
import subprocess
from pathlib import Path

from sixspec.core import Dimension
from sixspec.git.history import DimensionalGitHistory


@pytest.fixture
def git_repo_with_dimensional_commits(tmp_path):
    """Create a temporary git repo with dimensional commits."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()

    # Initialize git repo
    subprocess.run(['git', 'init'], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(
        ['git', 'config', 'user.email', 'test@example.com'],
        cwd=repo_path,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ['git', 'config', 'user.name', 'Test User'],
        cwd=repo_path,
        check=True,
        capture_output=True
    )

    # Create some files and commits
    commits = [
        {
            'file': 'payment.py',
            'msg': """fix: payment API timeout

WHY: Users abandoning carts at 25% rate due to timeout
HOW: Added retry logic with exponential backoff (3 attempts)
WHAT: Payment intent creation flow
WHERE: src/payment/stripe_integration.py"""
        },
        {
            'file': 'search.py',
            'msg': """feat: add search filters

WHY: Users cannot find products efficiently
HOW: Implemented faceted search with Elasticsearch
WHAT: Product search endpoint
WHERE: src/search/api.py
WHO: All users"""
        },
        {
            'file': 'validation.py',
            'msg': """refactor: extract payment validation

WHY: Code duplication across payment methods
HOW: Created shared validation module
WHERE: src/payment/validation.py, src/payment/stripe.py, src/payment/paypal.py"""
        },
        {
            'file': 'docs.md',
            'msg': """docs: update API documentation

WHY: Developers struggling to integrate payment API
HOW: Added code examples and troubleshooting guide
WHAT: Payment API documentation
WHERE: docs/api/payment.md
WHO: Third-party developers"""
        }
    ]

    for commit_data in commits:
        file_path = repo_path / commit_data['file']
        file_path.write_text(f"# {commit_data['file']}\n")
        subprocess.run(['git', 'add', commit_data['file']], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', commit_data['msg']],
            cwd=repo_path,
            check=True,
            capture_output=True
        )

    return repo_path


class TestDimensionalGitHistory:
    """Test dimensional git history querying."""

    def test_load_commits(self, git_repo_with_dimensional_commits):
        """Test loading commits from git repo."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        commits = history.commits
        assert len(commits) == 4

        # Commits should all have WHY and HOW
        for commit in commits:
            assert commit.has(Dimension.WHY)
            assert commit.has(Dimension.HOW)

    def test_query_by_where(self, git_repo_with_dimensional_commits):
        """Test querying by WHERE dimension."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        # Find all commits affecting payment
        payment_commits = history.query(where="payment")

        assert len(payment_commits) == 3  # fix, refactor, docs
        for commit in payment_commits:
            assert "payment" in commit.need(Dimension.WHERE).lower()

    def test_query_by_why(self, git_repo_with_dimensional_commits):
        """Test querying by WHY dimension."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        # Find commits related to users
        user_commits = history.query(why="users")

        assert len(user_commits) >= 2
        for commit in user_commits:
            assert "users" in commit.need(Dimension.WHY).lower()

    def test_query_by_commit_type(self, git_repo_with_dimensional_commits):
        """Test querying by commit type."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        # Find feature commits
        feat_commits = history.query(commit_type="feat")
        assert len(feat_commits) == 1
        assert feat_commits[0].commit_type == "feat"

        # Find fix commits
        fix_commits = history.query(commit_type="fix")
        assert len(fix_commits) == 1
        assert fix_commits[0].commit_type == "fix"

        # Find refactor commits
        refactor_commits = history.query(commit_type="refactor")
        assert len(refactor_commits) == 1
        assert refactor_commits[0].commit_type == "refactor"

    def test_query_multiple_dimensions(self, git_repo_with_dimensional_commits):
        """Test querying with multiple dimension filters."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        # Find payment-related fixes
        results = history.query(where="payment", commit_type="fix")

        assert len(results) == 1
        assert results[0].commit_type == "fix"
        assert "payment" in results[0].need(Dimension.WHERE).lower()

    def test_trace_file_purpose(self, git_repo_with_dimensional_commits):
        """Test tracing file purpose history."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        # Get commits affecting payment files
        commits = history.trace_file_purpose("payment")

        assert len(commits) >= 2
        # All should have WHY
        for commit in commits:
            assert commit.has(Dimension.WHY)

    def test_get_purposes(self, git_repo_with_dimensional_commits):
        """Test getting all unique purposes."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        purposes = history.get_purposes()

        assert len(purposes) == 4
        assert any("abandoning carts" in p for p in purposes)
        assert any("cannot find products" in p for p in purposes)

    def test_get_affected_files(self, git_repo_with_dimensional_commits):
        """Test getting all affected files."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        files = history.get_affected_files()

        assert len(files) >= 4
        assert any("stripe" in f for f in files)
        assert any("search" in f for f in files)

    def test_get_commit_types(self, git_repo_with_dimensional_commits):
        """Test getting all commit types."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        types = history.get_commit_types()

        assert set(types) == {'feat', 'fix', 'refactor', 'docs'}

    def test_reload_commits(self, git_repo_with_dimensional_commits):
        """Test reloading commits from git."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        initial_count = len(history.commits)

        # Add another commit
        test_file = git_repo_with_dimensional_commits / "newfile.py"
        test_file.write_text("# new file\n")
        subprocess.run(['git', 'add', 'newfile.py'], cwd=git_repo_with_dimensional_commits, check=True, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', """test: add new test

WHY: Need better test coverage
HOW: Added unit tests for payment module"""],
            cwd=git_repo_with_dimensional_commits,
            check=True,
            capture_output=True
        )

        # Should still have old count (cached)
        assert len(history.commits) == initial_count

        # After reload, should have new commit
        history.reload()
        assert len(history.commits) == initial_count + 1

    def test_case_insensitive_query(self, git_repo_with_dimensional_commits):
        """Test that queries are case-insensitive."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        results_lower = history.query(where="payment")
        results_upper = history.query(where="PAYMENT")
        results_mixed = history.query(where="PayMent")

        assert len(results_lower) == len(results_upper) == len(results_mixed)

    def test_empty_query_returns_all(self, git_repo_with_dimensional_commits):
        """Test that empty query returns all commits."""
        history = DimensionalGitHistory(git_repo_with_dimensional_commits)

        all_commits = history.query()
        assert len(all_commits) == 4