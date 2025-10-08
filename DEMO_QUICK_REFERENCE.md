# SixSpec Demo - Quick Reference Card

## 🎯 One-Liner Pitch
"SixSpec makes Git commits answer 'why does this code exist?' and traces that answer back to business mission."

## ⚡ Quick Demo (5 minutes)

### 1. Git Hook (1 min)
```bash
# Bad commit - rejected
git commit -m "fix: payment timeout"
❌ Missing WHY and HOW

# Good commit - accepted  
git commit -m "fix: payment timeout

WHY: Users abandoning carts at 25% rate
HOW: Added retry logic with exponential backoff"
✅ Commit accepted
```

### 2. Query History (2 min)
```python
from sixspec.git.history import DimensionalGitHistory

history = DimensionalGitHistory(Path("."))

# Query by purpose (not just file!)
history.query(why="timeout")
history.query(where="payment", commit_type="fix")

# Trace file evolution
history.trace_file_purpose("src/payment/stripe.py")
```

### 3. Provenance Chain (2 min)
```python
from sixspec.walkers.dilts_walker import DiltsWalker

walker = DiltsWalker(level=DiltsLevel.MISSION)
walker.execute(spec)

# Show WHAT→WHY chain
walker.trace_provenance()
# → ["Market leadership", "Premium tier", "Payment system", ...]
```

## 🔑 Key Concepts

### W5H1 Dimensions
- **WHO**: Actors, stakeholders
- **WHAT**: Actions, objects
- **WHEN**: Temporal context
- **WHERE**: Spatial context  
- **HOW**: Methods, implementation
- **WHY**: Purpose, motivation

### WHAT→WHY Propagation
```
Parent: WHAT = "Launch premium tier"
           ↓
Child:  WHY = "Launch premium tier"
        WHAT = "Build payment system"
```

### Dilts Hierarchy
```
L6: Mission     (Extreme autonomy - strategy)
L5: Identity    (High autonomy - who we are)
L4: Beliefs     (Moderate autonomy - principles)
L3: Capability  (Low autonomy - how we work)
L2: Behavior    (Very low autonomy - actions)
L1: Environment (Zero autonomy - execution)
```

## 📊 What's Working

✅ Git commit parser with WHY + HOW validation
✅ Git hook enforces dimensional format
✅ Queryable history by any dimension
✅ DiltsWalker with WHAT→WHY propagation  
✅ Portfolio execution (try multiple strategies)
✅ A2A task lifecycle (pause/resume)
✅ Hypergraph auto-organization
✅ Full test suite across all modules

## 🎬 Run the Demo

```bash
cd /home/Projects/SixSpec
python demo_anthropic.py
```

## 📁 Files to Show

**Core Logic:**
- `sixspec/core/models.py` - W5H1, Dimension, DiltsLevel
- `sixspec/walkers/dilts_walker.py` - WHAT→WHY propagation
- `sixspec/git/parser.py` - Commit parsing
- `sixspec/git/hooks/commit-msg` - Git hook validation

**Examples:**
- `examples/demo.py` - Git parsing demo
- `examples/hypergraph_demo.py` - Auto-organization
- `demo_anthropic.py` - Full showcase

**Docs:**
- `README.md` - Overview and quickstart
- `ARCHITECTURE.md` - System design
- `DESIGN_PHILOSOPHY.md` - Core principles

## 💡 Talking Points by Audience

### AI Researchers
- "Agents can trace decisions from goal to implementation"
- "WHAT→WHY chains enable explainable AI"
- "Validation over prediction for strategy selection"

### Product Teams
- "Git becomes queryable business knowledge base"
- "Search commits by purpose, not just files"
- "Self-documenting: history explains evolution"

### Engineers
- "Dimensional commits enforced at hook level"
- "Query: 'Show me all timeout-related fixes'"
- "Hierarchical delegation with provenance"

## 🤔 Anticipated Questions

**Q: Why not just better commit messages?**
A: We do! But structured + queryable. Git hook enforces it.

**Q: Just for commits or bigger?**
A: Commits are MVP. Framework extends to full agent coordination.

**Q: Performance?**
A: Lazy parsing, dimensional indices. Tested on 100+ commit repos.

**Q: Integration?**
A: Drop-in Git hook. Works with GitHub, GitLab, any Git workflow.

**Q: AI agent use cases?**
A: Context understanding, impact analysis, test generation, docs automation.

## 🚀 Next Steps

1. **Try it**: `python demo_anthropic.py`
2. **Explore code**: Browse `/home/Projects/SixSpec`
3. **Read docs**: Start with `README.md`
4. **Discuss**: Claude integration possibilities?

## 📈 Success Signals

✅ They ask to see the code
✅ They ask about Claude integration
✅ They discuss research implications
✅ They want to try it on their codebase

---

**Bottom Line**: Git history that's queryable, traceable, and AI-agent-friendly. Built on 20K lines of Python with comprehensive docs and tests.
