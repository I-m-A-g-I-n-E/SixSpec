#!/usr/bin/env python3
"""
Demonstration of SixSpec dimensional commit message parsing and querying.
"""

from pathlib import Path
from sixspec.core import Dimension
from sixspec.git.parser import CommitMessageParser


def demo_parsing():
    """Demonstrate parsing individual commit messages."""
    print("=" * 60)
    print("DEMO: Parsing Dimensional Commit Messages")
    print("=" * 60)

    commits = [
        """fix: payment API timeout

WHY: Users abandoning carts at 25% rate due to timeout
HOW: Added retry logic with exponential backoff (3 attempts)
WHAT: Payment intent creation flow
WHERE: src/payment/stripe_integration.py""",

        """feat: add search filters

WHY: Users cannot find products efficiently
HOW: Implemented faceted search with Elasticsearch
WHAT: Product search endpoint
WHERE: src/search/api.py
WHO: All users""",

        """refactor: extract payment validation

WHY: Code duplication across payment methods
HOW: Created shared validation module
WHERE: src/payment/validation.py, src/payment/stripe.py"""
    ]

    for i, msg in enumerate(commits, 1):
        print(f"\nCommit {i}:")
        print("-" * 40)

        commit = CommitMessageParser.parse(msg, f"hash{i:03d}")

        print(f"Type:   {commit.commit_type}")
        print(f"Title:  {commit.object}")
        print(f"Hash:   {commit.commit_hash}")
        print(f"\nWHY:    {commit.need(Dimension.WHY)}")
        print(f"HOW:    {commit.need(Dimension.HOW)}")

        if commit.has(Dimension.WHERE):
            print(f"WHERE:  {commit.need(Dimension.WHERE)}")

        if commit.has(Dimension.WHO):
            print(f"WHO:    {commit.need(Dimension.WHO)}")


def demo_validation():
    """Demonstrate commit message validation."""
    print("\n" + "=" * 60)
    print("DEMO: Commit Message Validation")
    print("=" * 60)

    test_cases = [
        ("Valid commit", """fix: something

WHY: Some reason
HOW: Some approach""", True),

        ("Missing WHY", """fix: something

HOW: Some approach""", False),

        ("Missing HOW", """fix: something

WHY: Some reason""", False),

        ("Invalid type", """invalid: something

WHY: Some reason
HOW: Some approach""", False),
    ]

    # Import validation function
    import sys
    from pathlib import Path
    hook_path = Path(__file__).parent.parent / "sixspec" / "git" / "hooks" / "commit-msg"
    with open(hook_path) as f:
        code = f.read()
    namespace = {}
    exec(code, namespace)
    validate_commit_message = namespace['validate_commit_message']

    for name, msg, expected_valid in test_cases:
        is_valid, errors = validate_commit_message(msg)

        status = "✓ PASS" if is_valid == expected_valid else "✗ FAIL"
        print(f"\n{status}: {name}")

        if errors:
            print(f"  Errors: {', '.join(errors)}")


def demo_querying():
    """Demonstrate querying git history (requires actual git repo)."""
    print("\n" + "=" * 60)
    print("DEMO: Querying Dimensional Git History")
    print("=" * 60)

    print("\nNote: This demo requires a git repository with dimensional commits.")
    print("See tests/git/test_history.py for working examples with test repos.")

    print("\nExample queries you can run:")
    print("""
from sixspec.git.history import DimensionalGitHistory

history = DimensionalGitHistory(Path("/path/to/repo"))

# Find commits by purpose
user_commits = history.query(why="user experience")

# Find commits affecting payment code
payment_commits = history.query(where="payment")

# Find bug fixes in payment code
payment_fixes = history.query(where="payment", commit_type="fix")

# Get all unique purposes
purposes = history.get_purposes()

# Trace a file's purpose history
commits = history.trace_file_purpose("src/payment/stripe.py")
for commit in commits:
    print(f"{commit.commit_hash}: {commit.need(Dimension.WHY)}")
    """)


if __name__ == "__main__":
    demo_parsing()
    demo_validation()
    demo_querying()

    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)