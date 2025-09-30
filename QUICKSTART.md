# SixSpec Quick Start Guide

Get started with dimensional commits in 5 minutes.

## Step 1: Install (30 seconds)

```bash
# Install the package
pip install -e .

# Verify installation
python -c "from sixspec.git.parser import CommitMessageParser; print('✓ SixSpec installed')"
```

## Step 2: Setup Git Hook (30 seconds)

```bash
# Copy the commit-msg hook to your repository
cp sixspec/git/hooks/commit-msg .git/hooks/
chmod +x .git/hooks/commit-msg

# Configure commit template (optional but recommended)
git config commit.template templates/.gitmessage

# Verify hook is installed
ls -l .git/hooks/commit-msg
```

## Step 3: Make Your First Dimensional Commit (2 minutes)

```bash
# Make a change
echo "# Test" > test.py
git add test.py

# Commit with dimensional format
git commit -m "test: add test file

WHY: Verify dimensional commit system is working
HOW: Created simple test file with git add and commit"
```

### What Happens

The git hook will:
1. ✅ Check commit type is valid (feat, fix, refactor, docs, test, chore)
2. ✅ Ensure WHY dimension is present
3. ✅ Ensure HOW dimension is present
4. ✅ Accept the commit if all checks pass
5. ❌ Reject with helpful error if anything is missing

### If Validation Fails

```bash
❌ Invalid commit message format:
  • Missing required dimension: WHY

📋 Commit messages must include WHY and HOW dimensions.
   See .gitmessage template for examples.
```

## Step 4: Query Your History (2 minutes)

```python
from pathlib import Path
from sixspec.git.history import DimensionalGitHistory
from sixspec.core import Dimension

# Load your repo
history = DimensionalGitHistory(Path("."))

# See all commits
print(f"Found {len(history.commits)} dimensional commits")

# Query by purpose
for commit in history.query(why="verify"):
    print(f"✓ {commit.object}")
    print(f"  WHY: {commit.need(Dimension.WHY)}")
    print(f"  HOW: {commit.need(Dimension.HOW)}")
```

## Common Patterns

### Bug Fix

```bash
git commit -m "fix: payment timeout issue

WHY: Users experiencing 25% cart abandonment due to API timeouts
HOW: Implemented retry logic with exponential backoff (3 attempts max)
WHERE: src/payment/stripe_integration.py"
```

### New Feature

```bash
git commit -m "feat: add search filters

WHY: Users cannot efficiently find products in large catalog
HOW: Implemented faceted search using Elasticsearch with category filters
WHERE: src/search/api.py, src/search/filters.py
WHO: All users"
```

### Refactoring

```bash
git commit -m "refactor: extract validation logic

WHY: Duplicated validation code across 3 payment providers
HOW: Created shared PaymentValidator class with common validation methods
WHERE: src/payment/validation.py, src/payment/stripe.py, src/payment/paypal.py"
```

### Documentation

```bash
git commit -m "docs: update API integration guide

WHY: Developers struggling with authentication flow (5 support tickets this week)
HOW: Added step-by-step guide with code examples and troubleshooting section
WHERE: docs/api/authentication.md
WHO: Third-party developers"
```

## Tips

### 1. Use the Template

```bash
# Load template in your editor
git commit --template=templates/.gitmessage

# Or set it as default
git config commit.template templates/.gitmessage
```

### 2. Optional Dimensions

Only WHY and HOW are required. Add others as needed:
- **WHAT**: Specific technical changes
- **WHERE**: Files or components affected
- **WHO**: Users or systems impacted
- **WHEN**: Conditions or triggers

### 3. Keep It Concise

```bash
# Good - clear and concise
WHY: Users abandoning carts due to timeout
HOW: Added retry logic with exponential backoff

# Too verbose
WHY: We noticed in our analytics dashboard that there has been a significant increase in cart abandonment rates, specifically around 25%, and after investigating the server logs we determined that the issue is related to API timeout errors occurring in the payment processing system...
```

### 4. Focus on Purpose

```bash
# Good - explains business value
WHY: Users cannot find products efficiently

# Bad - just repeats the change
WHY: Need to add search filters
```

## Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/git/test_parser.py

# Run specific test
pytest tests/git/test_parser.py::TestCommitMessageParser::test_parse_valid_commit_minimal
```

## Troubleshooting

### Hook Not Running

```bash
# Check hook is executable
ls -l .git/hooks/commit-msg

# If not, make it executable
chmod +x .git/hooks/commit-msg

# Check hook has correct shebang
head -1 .git/hooks/commit-msg
# Should show: #!/usr/bin/env python3
```

### Import Errors

```bash
# Reinstall in development mode
pip install -e .

# Verify Python can find sixspec
python -c "import sixspec; print(sixspec.__file__)"
```

### Invalid Format But Looks Correct

```bash
# Check dimensions are uppercase
WHY: (correct)
why: (incorrect)

# Check commit type is valid
feat: (correct)
feature: (incorrect)

# Valid types: feat, fix, refactor, docs, test, chore
```

## Next Steps

1. **Read Full Documentation**: See `README.md` for complete API reference
2. **Run Demo**: `python examples/demo.py` to see examples
3. **Review Tests**: `tests/git/` for more examples
4. **Query Your History**: Use `DimensionalGitHistory` to explore commits

## Help

Having issues? Common questions:

**Q: Can I use this with existing repositories?**
A: Yes! Just install the hook. Old commits won't have dimensions, but new ones will. Use `skip_invalid=True` when querying.

**Q: What about merge commits?**
A: Merge commits are automatically skipped by the validation hook.

**Q: Can I temporarily bypass the hook?**
A: Use `git commit --no-verify` to skip hooks (not recommended for normal use).

**Q: Do dimensions need to be in a specific order?**
A: No, any order works. Only the subject line must be first.

**Q: Can I have multi-line dimension values?**
A: Currently single-line only. Keep dimensions concise.

---

**Ready to go?** Start committing with dimensions and make your Git history queryable!