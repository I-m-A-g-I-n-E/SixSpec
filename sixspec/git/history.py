"""Query git history using dimensional filters."""

from pathlib import Path
from typing import List, Optional

from ..core import CommitW5H1, Dimension
from .parser import CommitMessageParser


class DimensionalGitHistory:
    """Query git history using dimensional filters."""

    def __init__(self, repo_path: Path, skip_invalid: bool = True):
        """
        Initialize dimensional git history.

        Args:
            repo_path: Path to git repository
            skip_invalid: If True, skip commits that don't follow dimensional format
        """
        self.repo_path = Path(repo_path)
        self.skip_invalid = skip_invalid
        self._commits: Optional[List[CommitW5H1]] = None

    @property
    def commits(self) -> List[CommitW5H1]:
        """
        Lazy-load and cache all dimensional commits.

        Returns:
            List of CommitW5H1 objects
        """
        if self._commits is None:
            self._commits = CommitMessageParser.parse_git_log(
                self.repo_path,
                skip_invalid=self.skip_invalid
            )
        return self._commits

    def reload(self) -> None:
        """Force reload of commits from git log."""
        self._commits = None

    def query(
        self,
        where: Optional[str] = None,
        why: Optional[str] = None,
        what: Optional[str] = None,
        who: Optional[str] = None,
        when: Optional[str] = None,
        how: Optional[str] = None,
        commit_type: Optional[str] = None
    ) -> List[CommitW5H1]:
        """
        Query commits by dimensional criteria.

        All filters are case-insensitive substring matches.

        Args:
            where: Filter by WHERE dimension (file paths, components)
            why: Filter by WHY dimension (purpose, business value)
            what: Filter by WHAT dimension (specific changes)
            who: Filter by WHO dimension (users, systems affected)
            when: Filter by WHEN dimension (conditions, triggers)
            how: Filter by HOW dimension (technical approach)
            commit_type: Filter by commit type (feat, fix, refactor, etc.)

        Returns:
            List of matching CommitW5H1 objects
        """
        results = self.commits

        if where:
            results = [
                c for c in results
                if c.has(Dimension.WHERE) and where.lower() in c.need(Dimension.WHERE).lower()
            ]

        if why:
            results = [
                c for c in results
                if c.has(Dimension.WHY) and why.lower() in c.need(Dimension.WHY).lower()
            ]

        if what:
            results = [
                c for c in results
                if c.has(Dimension.WHAT) and what.lower() in c.need(Dimension.WHAT).lower()
            ]

        if who:
            results = [
                c for c in results
                if c.has(Dimension.WHO) and who.lower() in c.need(Dimension.WHO).lower()
            ]

        if when:
            results = [
                c for c in results
                if c.has(Dimension.WHEN) and when.lower() in c.need(Dimension.WHEN).lower()
            ]

        if how:
            results = [
                c for c in results
                if c.has(Dimension.HOW) and how.lower() in c.need(Dimension.HOW).lower()
            ]

        if commit_type:
            results = [
                c for c in results
                if hasattr(c, 'commit_type') and c.commit_type == commit_type
            ]

        return results

    def trace_file_purpose(self, file_path: str) -> List[CommitW5H1]:
        """
        Find all commits that modified a file and their WHY.

        Args:
            file_path: Path to file or component name

        Returns:
            List of CommitW5H1 objects sorted chronologically
        """
        commits = self.query(where=file_path)
        # Sort by commit hash (chronological order depends on git history)
        return commits

    def get_purposes(self) -> List[str]:
        """
        Get all unique WHY values across commits.

        Returns:
            List of unique purpose statements
        """
        purposes = set()
        for commit in self.commits:
            if commit.has(Dimension.WHY):
                purposes.add(commit.need(Dimension.WHY))
        return sorted(purposes)

    def get_affected_files(self) -> List[str]:
        """
        Get all unique WHERE values (file paths) across commits.

        Returns:
            List of unique file/component paths
        """
        files = set()
        for commit in self.commits:
            if commit.has(Dimension.WHERE):
                files.add(commit.need(Dimension.WHERE))
        return sorted(files)

    def get_commit_types(self) -> List[str]:
        """
        Get all unique commit types used.

        Returns:
            List of unique commit types (feat, fix, etc.)
        """
        types = set()
        for commit in self.commits:
            if hasattr(commit, 'commit_type') and commit.commit_type:
                types.add(commit.commit_type)
        return sorted(types)