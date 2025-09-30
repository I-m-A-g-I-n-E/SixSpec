"""Parse dimensional commit messages into CommitW5H1 objects."""

import re
import subprocess
from pathlib import Path
from typing import List, Optional

from ..core import CommitW5H1, Dimension


class CommitMessageParser:
    """Parse dimensional commit messages into CommitW5H1 objects."""

    DIMENSION_PATTERN = re.compile(
        r'^(WHO|WHAT|WHEN|WHERE|HOW|WHY):\s*(.+)$',
        re.MULTILINE
    )

    SUBJECT_PATTERN = re.compile(r'^(\w+):\s*(.+)$')

    @classmethod
    def parse(cls, commit_msg: str, commit_hash: str = "") -> CommitW5H1:
        """
        Parse commit message into CommitW5H1 object.

        Args:
            commit_msg: The commit message text
            commit_hash: The git commit hash (optional)

        Returns:
            CommitW5H1 object

        Raises:
            ValueError: If message format is invalid
        """
        # Remove comment lines
        lines = [line for line in commit_msg.split('\n') if not line.strip().startswith('#')]
        clean_msg = '\n'.join(lines).strip()

        if not clean_msg:
            raise ValueError("Empty commit message")

        # Extract subject line
        subject_line = clean_msg.split('\n')[0].strip()

        # Parse type and subject
        match = cls.SUBJECT_PATTERN.match(subject_line)
        if not match:
            raise ValueError(f"Invalid subject line format: {subject_line}")

        commit_type, subject = match.groups()

        # Extract dimensions
        dimensions = {}
        for match in cls.DIMENSION_PATTERN.finditer(clean_msg):
            dim_name, dim_value = match.groups()
            dimensions[Dimension[dim_name]] = dim_value.strip()

        # Validate required dimensions
        if Dimension.WHY not in dimensions:
            raise ValueError("Missing required dimension: WHY")
        if Dimension.HOW not in dimensions:
            raise ValueError("Missing required dimension: HOW")

        # Store commit metadata in special dimensions
        # Use WHAT for commit type if not already set
        if Dimension.WHAT not in dimensions:
            dimensions[Dimension.WHAT] = f"{commit_type}: {subject}"

        # Store commit hash in WHERE if not already set (can be overridden by explicit WHERE)
        if commit_hash and Dimension.WHEN not in dimensions:
            dimensions[Dimension.WHEN] = f"commit {commit_hash[:8]}"

        # Create CommitW5H1
        commit = CommitW5H1(
            subject=commit_type,
            predicate="changes",
            object=subject,
            dimensions=dimensions
        )

        # Store commit metadata as attributes for convenience
        commit.commit_hash = commit_hash
        commit.commit_type = commit_type

        return commit

    @classmethod
    def parse_git_log(
        cls,
        repo_path: Path,
        n: Optional[int] = None,
        skip_invalid: bool = True
    ) -> List[CommitW5H1]:
        """
        Parse recent commits from git log.

        Args:
            repo_path: Path to git repository
            n: Number of commits to fetch (None for all)
            skip_invalid: If True, skip commits that don't follow format.
                         If False, raise ValueError on invalid commits.

        Returns:
            List of CommitW5H1 objects
        """
        cmd = ['git', 'log', '--format=%H%n%B%n---END---']
        if n:
            cmd.extend(['-n', str(n)])

        try:
            result = subprocess.run(
                cmd,
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Git command failed: {e.stderr}")

        commits = []
        for commit_block in result.stdout.split('---END---'):
            if not commit_block.strip():
                continue

            lines = commit_block.strip().split('\n')
            commit_hash = lines[0]
            commit_msg = '\n'.join(lines[1:])

            try:
                commit = cls.parse(commit_msg, commit_hash)
                commits.append(commit)
            except ValueError as e:
                if not skip_invalid:
                    raise ValueError(f"Invalid commit {commit_hash}: {e}")
                # Skip commits that don't follow format
                continue

        return commits