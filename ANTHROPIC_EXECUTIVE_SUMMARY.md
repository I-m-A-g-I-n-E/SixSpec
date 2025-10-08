# SixSpec: Executive Summary for Anthropic

## What Is SixSpec?

A dimensional specification framework that makes Git history queryable and creates traceable provenance chains from business mission to code implementation.

**In One Sentence**: SixSpec turns your Git log into a queryable knowledge base where every commit explains *why* it exists, not just *what* changed.

## The Problem

1. **Context Loss**: Code changes happen but the reasoning disappears
2. **Purpose Fragmentation**: Requirements, design, and implementation live in silos
3. **Agent Blindness**: AI agents can read code syntax but not understand *why* it exists

## The Solution

### 1. Dimensional Commits (W5H1)

Every Git commit captures six dimensions:
- **WHY**: Purpose, business value
- **HOW**: Technical approach  
- **WHAT**: Specific changes
- **WHERE**: Files/components
- **WHO**: Users/systems affected
- **WHEN**: Conditions/triggers

**Git hook enforces** WHY + HOW at commit time.

### 2. Queryable History

```python
history.query(why="timeout")           # All timeout-related commits
history.query(where="payment")         # All payment code changes
history.trace_file_purpose("file.py") # Why does this file exist?
```

Search by *purpose* and *approach*, not just files and text.

### 3. WHAT→WHY Provenance Chains

```
Mission (L6):     WHAT = "Market leadership"
                           ↓
Identity (L5):    WHY = "Market leadership"
                  WHAT = "Premium tier"
                           ↓
Capability (L3):  WHY = "Premium tier"
                  WHAT = "Payment system"
                           ↓
Environment (L1): WHY = "Payment system"
                  WHAT = "WebhookController"
                           → EXECUTES
```

Every action traces back to business mission. Ask "why does this code exist?" at any level.

## What's Built (20K lines, fully documented)

✅ **Git Integration** - Parser, hooks, queryable history
✅ **Core Framework** - W5H1 specs, Dilts hierarchy, confidence tracking
✅ **Walker Architecture** - Hierarchical delegation with WHAT→WHY
✅ **A2A Protocol** - Graceful pause/resume for long-running tasks
✅ **Hypergraph** - Auto-organization based on shared dimensions
✅ **Test Suite** - Comprehensive coverage across all modules

## Why Anthropic Should Care

### 1. Agent-Friendly Infrastructure
- Claude can query Git history to understand *why* code exists
- Dimensional search enables context-aware code generation
- WHAT→WHY chains provide explainable AI reasoning

### 2. Provenance Tracking
- Every action traces to original purpose
- Solves "why did the AI do that?" problem
- Full audit trail from goal to implementation

### 3. Context Preservation
- A2A protocol enables graceful interruption
- Long-running AI tasks can pause/resume without losing context
- Hierarchical task coordination between agents

### 4. Empirical Validation
- Portfolio execution: try multiple strategies, validate, pick winner
- Measure results instead of predicting confidence
- Aligns with ML mindset: test, don't guess

### 5. Self-Documenting Systems
- Git history becomes queryable knowledge base
- Reduces reliance on stale documentation
- Purpose and approach captured at commit time

## Immediate Use Cases for Claude

1. **Context Understanding**: Query history before suggesting changes
2. **Impact Analysis**: "What would be affected by changing auth?"
3. **Test Generation**: Read HOW dimension to know what to test
4. **Documentation**: Auto-generate docs from WHY dimensions
5. **Explainable Generation**: "I wrote this because..." + provenance chain

## Demo Flow (5 minutes)

1. **Git Hook** (1 min): Show commit rejection/acceptance
2. **Query History** (2 min): Search by purpose, trace file evolution
3. **Provenance** (2 min): Show WHAT→WHY chain from mission to code

Optional deep dives:
- Hypergraph auto-organization
- Portfolio execution with validation
- A2A task lifecycle

## Technical Highlights

**Core Pattern**: Parent's WHAT becomes child's WHY
**Architecture**: 6-layer hierarchy (Core → Agents → Walkers → Integration)
**Data Model**: Subject-predicate-object triples with six dimensions
**Execution**: Portfolio tries multiple strategies, validates empirically
**Integration**: Drop-in Git hooks, Python API, works with any workflow

## Next Steps

### Immediate Opportunities
1. **Claude Integration Demo** - Show Claude querying dimensional history
2. **Agent Coordination** - Multi-Claude instances using A2A protocol
3. **Codebase Understanding** - Claude analyzes commits to explain evolution

### Research Directions
1. **Provenance in LLM Reasoning** - Apply WHAT→WHY to chain-of-thought
2. **Multi-Agent Validation** - Portfolio execution with LLM-generated solutions
3. **Dimensional Context Compression** - Use W5H1 to reduce token usage

## The Ask

**Short term**: Feedback on architecture and Claude integration possibilities

**Medium term**: Explore collaboration on:
- Making Claude dimensional-history-aware
- Agent coordination protocols
- Provenance tracking in AI reasoning

**Long term**: SixSpec as infrastructure for explainable, traceable AI agent ecosystems

## Resources

- **Full Demo**: `/home/Projects/SixSpec/demo_anthropic.py`
- **Documentation**: 31 markdown files covering architecture, philosophy, APIs
- **Code**: ~20K lines across 6 modules with comprehensive tests
- **Strategy**: `ANTHROPIC_DEMO_STRATEGY.md` (detailed demo guide)
- **Quick Ref**: `DEMO_QUICK_REFERENCE.md` (talking points)

---

**Bottom Line**: Infrastructure for AI agents to understand *why* code exists, trace decisions to business goals, and provide explainable reasoning. Git integration is the MVP - full framework enables agent ecosystems with traceable provenance.

**Contact**: Ready to discuss Claude integration and research collaboration.
