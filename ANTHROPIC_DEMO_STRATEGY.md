# SixSpec: Anthropic Demo Strategy

## Executive Summary

**What We've Built**: A dimensional specification framework that makes Git history queryable, context traceable, and AI-agent-friendly by capturing the *why* and *how* of every change.

**The Hook**: "What if your Git commits could answer 'why does this code exist?' and trace that answer all the way back to business mission?"

**Demo Time**: 5-7 minutes
**Technical Depth**: Can scale from surface-level to deep architecture discussion

---

## The Minimum Viable Demo

### Core Value Proposition (30 seconds)

**The Problem SixSpec Solves:**
1. **Context Loss**: Code changes happen, but reasoning disappears
2. **Purpose Fragmentation**: Requirements, design, implementation live in different silos  
3. **Agent Blindness**: AI agents can read code syntax but not understand *why* it exists

**The SixSpec Solution:**
- Dimensional commits (W5H1: Who, What, When, Where, How, Why)
- WHAT→WHY propagation (parent's WHAT becomes child's WHY)
- Queryable Git history that's both human and AI-agent readable

---

## Demo Flow: 3-Act Structure

### Act 1: The Git Hook (90 seconds)
**Show the immediate value**

**Live Demo:**
```bash
# Make a bad commit (missing WHY/HOW)
git commit -m "fix: payment timeout"

# Hook rejects it ❌
❌ Missing required dimension: WHY
❌ Missing required dimension: HOW

# Make a dimensional commit
git commit -m "fix: payment timeout

WHY: Users abandoning carts at 25% rate due to timeout
HOW: Added retry logic with exponential backoff (3 attempts)
WHERE: src/payment/stripe_integration.py"

# Hook accepts it ✅
```

**Key Point**: "Every commit now captures both *what changed* and *why it matters*. Your Git history becomes living documentation."

**Anthropic Hook**: This is infrastructure for AI agents to understand codebase evolution with full context, not just diffs.


### Act 2: Queryable History (2 minutes)
**Show the power of dimensional search**

**Live Demo - Run Python REPL:**
```python
from pathlib import Path
from sixspec.git.history import DimensionalGitHistory
from sixspec.core import Dimension

# Load your Git history
history = DimensionalGitHistory(Path("."))

# Query by PURPOSE (not just file/text)
timeout_fixes = history.query(why="timeout")
for commit in timeout_fixes:
    print(f"{commit.commit_hash[:7]}: {commit.object}")
    print(f"  WHY: {commit.need(Dimension.WHY)}")
    print(f"  HOW: {commit.need(Dimension.HOW)}")

# Query by affected area + type
payment_bugs = history.query(where="payment", commit_type="fix")

# Trace a file's PURPOSE evolution
file_history = history.trace_file_purpose("src/payment/stripe.py")
for commit in file_history:
    print(f"{commit.need(Dimension.WHY)} → {commit.need(Dimension.HOW)}")

# Get all unique business purposes in the codebase
purposes = history.get_purposes()
print(f"This codebase exists to: {purposes}")
```

**Key Points:**
- "Traditional Git: search by text/file. SixSpec: search by *purpose* and *approach*"
- "Answer questions like: 'Show me all timeout-related fixes' or 'Why does this file exist?'"
- "Perfect for AI agents doing impact analysis or understanding context before generating code"

**Anthropic Hook**: Claude could query this to understand *why* a codebase evolved the way it did, not just *what* changed.


### Act 3: The Full Framework (2-3 minutes)
**Show the vision: hierarchical provenance with WHAT→WHY chains**

**Visual/Code Demo:**
```python
from sixspec.walkers.dilts_walker import DiltsWalker
from sixspec.core import Chunk, Dimension, DiltsLevel

# Mission-level walker (highest autonomy)
mission = DiltsWalker(level=DiltsLevel.MISSION)

# Define top-level mission
spec = Chunk(
    subject="Company",
    predicate="needs",
    object="market leadership",
    dimensions={
        Dimension.WHAT: "Achieve market leadership in payments"
    }
)

# Execute - automatically delegates down hierarchy
result = mission.execute(spec)

# Now traverse to the deepest implementation
walker = mission
while walker.children:
    walker = walker.children[0]

# Trace the full provenance chain
provenance = walker.trace_provenance()
print("Purpose chain from mission to implementation:")
for i, purpose in enumerate(provenance):
    print(f"  L{6-i}: {purpose}")

# Output shows complete WHAT→WHY chain:
# L6: "Achieve market leadership in payments"
# L5: "Launch premium subscription tier"  
# L4: "Build reliable payment processing"
# L3: "Integrate Stripe API"
# L2: "Implement webhook handlers"
# L1: "Write WebhookController.handle_payment()"
```

**Key Points:**
- "Every line of code can trace its purpose back to business mission"
- "Parent's WHAT becomes child's WHY - creates unbreakable provenance chain"
- "Six levels of delegation (Mission → Identity → Beliefs → Capability → Behavior → Environment)"
- "Each level has different autonomy: Mission has extreme freedom, Environment just executes"

**Anthropic Hook**: 
- AI agents can understand *why* they're doing something at every level
- Enables explainable AI: "Why did you generate this code?" → "Because mission was X, which required Y, which needed Z"
- Graceful interruption: pause/resume with full context preservation


---

## Deep Dive Options (If Interest Shown)

### 1. Hypergraph Auto-Organization (2 min)
**The "Grocery Store Rule"**

```python
from sixspec.core.hypergraph import SpecificationHypergraph
from sixspec.core import Chunk, Dimension

graph = SpecificationHypergraph()

# Add tasks that share dimensions
milk = Chunk("User", "buys", "milk", 
    dimensions={Dimension.WHERE: "grocery", Dimension.WHEN: "today"})
bread = Chunk("User", "buys", "bread",
    dimensions={Dimension.WHERE: "grocery", Dimension.WHEN: "today"})
hammer = Chunk("User", "buys", "hammer",
    dimensions={Dimension.WHERE: "hardware", Dimension.WHEN: "today"})

graph.add_object(milk)
graph.add_object(bread)
graph.add_object(hammer)

# Auto-organization: specs sharing ≥1 dimension cluster together
clusters = graph.find_clusters()  
# → 2 clusters: [milk, bread] and [hammer]

# Auto-generate hierarchy: Epic → Story → Task
hierarchy = graph.organize_hierarchy()
# → Epic: "Today at Grocery" contains Story: [milk, bread]
# → Epic: "Today at Hardware" contains Story: [hammer]
```

**Key Points:**
- "Specifications self-organize based on shared context"
- "No manual epic/story creation - emerges from dimensional overlap"
- "Perfect for AI agents: 'Give me all grocery-related tasks' auto-clusters"

### 2. Portfolio Execution with Validation (2 min)
**Choose strategies by results, not predictions**

```python
from sixspec.walkers.dilts_walker import DiltsWalker, ValidationResult

class CapabilityWalker(DiltsWalker):
    def generate_strategies(self, spec, n):
        # Generate 3 different approaches
        return [
            "Integrate Stripe",
            "Integrate PayPal", 
            "Build custom processor"
        ]
    
    def validate(self, result):
        # Validate actual results
        test_coverage = run_tests(result)
        return ValidationResult(
            score=test_coverage,
            passed=test_coverage > 0.8
        )

walker = CapabilityWalker(level=DiltsLevel.CAPABILITY)
result = walker.execute_portfolio(spec, n_strategies=3)
# → Tries all 3, picks winner based on validation score
```

**Key Points:**
- "Don't predict which strategy is best - try them and measure"
- "Each strategy executed in isolated workspace"
- "Winner selected by validation score, not confidence"
- "Enables AI agents to explore multiple approaches safely"


### 3. A2A Task Lifecycle (2 min)
**Graceful interruption with context preservation**

```python
from sixspec.walkers.a2a_walker import A2AWalker
from sixspec.a2a import TaskStatus

walker = A2AWalker(level=DiltsLevel.CAPABILITY)
spec = Chunk("System", "needs", "payment",
    dimensions={Dimension.WHAT: "Integrate payment processing"})

# Start execution
walker.task.start()
walker.execute(spec)

# User interrupts - gracefully pause
walker.pause()  # Cascades to all children

# Task preserves:
# - Full WHAT→WHY chain
# - Workspace data
# - Execution position
# - Child task states

# Inspect progress while paused
progress = walker.get_progress()
print(f"Level: {progress['level']}")
print(f"WHAT: {progress['what']}")  
print(f"WHY: {progress['why']}")
print(f"Provenance: {progress['provenance']}")

# Resume later - continues exactly where it left off
walker.resume()
```

**Key Points:**
- "Based on Google's A2A protocol for agent-to-agent coordination"
- "Pause/resume without losing context - critical for long-running AI tasks"
- "Hierarchical coordination: parent knows when children pause/fail"
- "Real-time status streaming for monitoring"

---

## Why Anthropic Should Care

### 1. **Agent-Friendly Infrastructure**
- Claude can query Git history to understand *why* code exists, not just *what* it does
- WHAT→WHY chains provide explainable reasoning for code generation
- Dimensional search enables context-aware assistance

### 2. **Provenance Tracking**
- Every action traces back to mission/purpose
- Solves the "why did the AI do that?" problem
- Full audit trail from strategic goal to ground implementation

### 3. **Context Preservation**
- A2A protocol enables long-running tasks with graceful interruption
- Critical for complex AI workflows that can't complete in one shot
- Resume with full context - no "remind me what we were doing"

### 4. **Validation Over Prediction**
- Portfolio execution tries multiple approaches, validates results
- Aligns with empirical ML mindset: measure, don't guess
- AI agents can safely explore solution space

### 5. **Self-Documenting Systems**
- Git commits become queryable knowledge base
- Reduces reliance on stale documentation
- History answers "why does this exist?" automatically

---

## Technical Architecture Highlights

### Core Innovation: WHAT→WHY Propagation
```
Mission:     WHAT = "Market leadership"
               ↓
Identity:    WHY = "Market leadership"
             WHAT = "Premium tier"
               ↓
Beliefs:     WHY = "Premium tier"
             WHAT = "Payment system"
               ↓
[continues 3 more levels to ground execution]
```

**Result**: Unbreakable provenance chain from business value to implementation.


### Data Structures

**Chunk (W5H1)**
- Subject-predicate-object triple (RDF-style)
- Six dimensions with per-dimension confidence scores
- Lazy evaluation via `need()` method
- Immutable updates via `copy_with()`

**DiltsLevel Enum**
- 6 levels from Environment (L1) to Mission (L6)
- Each level has autonomy gradient and primary dimensions
- Natural mapping to organizational hierarchy

**Specialized Chunks**
- CommitChunk: Requires WHY + HOW (Git commits)
- SpecChunk: Requires WHO + WHAT + WHY (full specs)

### Agent Architecture

**NodeAgent**: Isolated processing
- TreeSitter parsing
- Linting
- Single-file operations

**GraphAgent**: Context-aware traversal
- Dependency analysis
- Impact analysis
- Relationship discovery

**DiltsWalker**: Hierarchical delegation
- WHAT→WHY propagation
- Portfolio execution
- Provenance tracing

**A2AWalker**: Task lifecycle
- Pause/resume
- Parent-child coordination
- Real-time status

---

## The Codebase Stats

- **~20,000 lines of Python**
- **31 markdown docs** (comprehensive documentation)
- **6 core modules**: core, agents, walkers, a2a, git, hypergraph
- **Comprehensive test suite** across all modules
- **3 working demos**: git parsing, hypergraph, A2A lifecycle

### What's Implemented & Working

✅ **Phase 1: Git Integration (Complete)**
- Dimensional commit message parser
- Git hook validation (enforces WHY + HOW)
- Queryable Git history with dimensional search
- Commit message template
- Full test coverage

✅ **Phase 2: Core Framework (Complete)**
- W5H1 dimensional specifications
- Dilts hierarchy with 6 levels
- WHAT→WHY propagation
- Confidence tracking per dimension
- "Grocery store rule" clustering

✅ **Phase 3: Walker Architecture (Complete)**
- DiltsWalker with hierarchical delegation
- Portfolio execution with validation
- Provenance tracing
- Workspace isolation
- Strategy pattern for level-specific behavior

✅ **Phase 4: A2A Integration (Complete)**
- Task lifecycle states (pending → running → paused → completed)
- Graceful pause/resume
- Parent-child coordination
- Status streaming
- Context preservation

✅ **Phase 5: Hypergraph Organization (Complete)**
- Auto-clustering based on shared dimensions
- Epic/story/task hierarchy generation
- Dimensional similarity detection
- Graph-based relationship discovery

---

## Demo Preparation Checklist

### Files to Have Ready

1. **Live terminal** for git hook demo
2. **Python REPL** for history queries
3. **VS Code** showing:
   - `sixspec/git/parser.py` (commit parsing)
   - `sixspec/walkers/dilts_walker.py` (WHAT→WHY propagation)
   - `examples/hypergraph_demo.py` (grocery store example)

### Example Commits to Show

Create a mini repo with dimensional commits about payment features:

```bash
# Commit 1
git commit -m "feat: add payment processing

WHY: Enable premium subscriptions per Q2 roadmap
HOW: Integrated Stripe Checkout Sessions API
WHERE: src/payment/stripe.py
WHO: Premium users"

# Commit 2  
git commit -m "fix: payment timeout

WHY: Users abandoning carts at 25% rate
HOW: Added retry logic with exponential backoff (3 attempts)
WHERE: src/payment/stripe.py"

# Commit 3
git commit -m "refactor: extract validation

WHY: Duplicated validation across Stripe and PayPal integrations
HOW: Created shared PaymentValidator class
WHERE: src/payment/validation.py, src/payment/stripe.py"
```

Then query:
- `history.query(where="payment")` → Shows all 3
- `history.query(why="timeout")` → Shows commit 2
- `history.trace_file_purpose("src/payment/stripe.py")` → Shows evolution


---

## Talking Points by Audience Type

### If Talking to AI Research Team

**Focus on:**
- Agent-friendly provenance: "Every action explains its purpose"
- Explainable AI: "Trace decisions from mission to implementation"  
- Portfolio validation: "Measure results, don't predict confidence"
- Context preservation: "A2A protocol enables long-running tasks"

**Hook**: "What if agents could understand *why* code exists, not just *what* it does?"

### If Talking to Product Team

**Focus on:**
- Queryable Git history: "Search commits by business purpose"
- Self-documenting: "History becomes living documentation"
- Impact analysis: "What commits touched payments? What was the business reason?"
- Developer velocity: "Stop asking 'why does this exist?' - Git knows"

**Hook**: "Turn your Git log into a queryable knowledge base of business decisions."

### If Talking to Engineering Team

**Focus on:**
- Git hook validation: "Enforces WHY + HOW at commit time"
- Dimensional queries: "Search by purpose, not just file/text"
- Hierarchical delegation: "Dilts levels map to autonomy gradient"
- Portfolio execution: "Try multiple strategies, validate, pick winner"

**Hook**: "Make your Git history as queryable as your database."

### If Talking to Research Scientists

**Focus on:**
- W5H1 dimensional model: "Universal specification framework"
- Graph-based organization: "Auto-clustering via shared dimensions"
- Confidence tracking: "Per-dimension uncertainty quantification"
- Validation over prediction: "Empirical selection of strategies"

**Hook**: "A formal system for tracing provenance in hierarchical decision-making."

---

## Anticipated Questions & Answers

### Q: "Why not just use better commit messages?"

**A**: We do! But SixSpec makes them *structured* and *queryable*. 

Traditional: "Fixed the payment thing" (vague)
Better: "Fixed payment timeout by adding retry logic" (clear but not queryable)
SixSpec: WHY + HOW as first-class dimensions (structured, searchable, agent-readable)

Plus: Git hook enforces the structure. No more vague commits.

### Q: "Is this just for commits, or bigger systems?"

**A**: Commits are the MVP - immediate value, low friction adoption.

But the framework extends to:
- Full hierarchical delegation (mission → implementation)
- Portfolio execution with multiple strategies
- Hypergraph organization of any specs
- AI agent coordination with A2A protocol

Git integration proves the concept. Full framework enables agent ecosystems.

### Q: "What about performance with large repos?"

**A**: 
- Parsing is lazy: only parse commits you query
- Dimensional indices: pre-index by dimension for fast queries
- Graph traversal: NetworkX for efficient clustering
- Workspace isolation: each walker has independent state

Currently tested on repos with 100+ commits. Scales linearly with index optimization.

### Q: "How does this integrate with existing tools?"

**A**:
- **Git**: Drop-in hook, works with any Git workflow
- **GitHub/GitLab**: Commit format visible in web UI
- **CI/CD**: Query history in pipelines for impact analysis
- **IDEs**: VSCode extension could show dimensional search
- **AI agents**: Claude/GPT can query via Python API

Non-invasive: enhances Git, doesn't replace it.

### Q: "What if developers don't write good WHY/HOW?"

**A**: Three-level defense:

1. **Git hook rejection**: Won't accept commit without WHY/HOW
2. **Template guidance**: `.gitmessage` shows examples
3. **Query visibility**: Bad WHY stands out when you search history

Plus: Cultural shift. When you can query "show me all user experience improvements," people want their commits to show up.

### Q: "Is this trying to replace requirements management?"

**A**: No - it *connects* requirements to implementation.

Requirements tools: "We need payments"
SixSpec: "This commit implements payments *because* requirements said so"

Creates traceable chain: Requirement → Design → Commit → Code
Each level's WHAT becomes next level's WHY.

### Q: "What about AI agent use cases specifically?"

**A**: Four immediate uses:

1. **Context understanding**: Agent queries history before suggesting changes
2. **Impact analysis**: "What commits would be affected by changing authentication?"
3. **Test generation**: Agent reads HOW dimension to know what to test
4. **Documentation**: Auto-generate docs from WHY dimensions

Future: Agents use full Dilts framework for hierarchical planning with provenance.


---

## Follow-Up Opportunities

### Immediate Collaboration Ideas

1. **Claude Integration Demo**
   - Claude queries dimensional Git history for context
   - Generates commits with proper WHY/HOW
   - Uses provenance chain for explainable code generation

2. **Agent Coordination Protocol**
   - Multiple Claude instances coordinating via A2A
   - Hierarchical task delegation with WHAT→WHY
   - Graceful pause/resume for long-running tasks

3. **Codebase Understanding**
   - Claude analyzes dimensional commits to understand evolution
   - Generates documentation from WHY dimensions
   - Answers "why does this exist?" from Git history

### Research Directions

1. **Provenance in LLM Reasoning**
   - Apply WHAT→WHY chains to LLM decision-making
   - Make chain-of-thought traceable to original prompt
   - Enable "why did you generate this?" queries

2. **Multi-Agent Validation**
   - Portfolio execution with LLM agents
   - Generate multiple solutions, validate, pick winner
   - Empirical selection over confidence scoring

3. **Dimensional Context Windows**
   - Use W5H1 to compress context more efficiently
   - "This code exists WHY: X, implemented HOW: Y"
   - Fewer tokens for same semantic content

---

## Success Metrics for Demo

### Immediate Engagement Signals

✅ **They ask to see the code** → Technical interest
✅ **They ask about Claude integration** → Product interest  
✅ **They discuss research implications** → Scientific interest
✅ **They want to try it on their codebase** → Adoption interest

### Key Messages Delivered

✅ Git history can be queryable and agent-friendly
✅ WHAT→WHY propagation creates provenance chains
✅ Validation beats prediction for strategy selection
✅ A2A protocol enables graceful task coordination

### Follow-Up Actions

- Share GitHub repo for exploration
- Schedule technical deep-dive on specific modules
- Discuss Claude integration possibilities
- Explore research collaboration on provenance

---

## One-Liner Hooks (By Context)

**Elevator pitch**: 
"SixSpec makes Git commits answer 'why does this code exist?' and traces that answer back to business mission."

**Technical pitch**:
"Dimensional specifications with WHAT→WHY propagation create queryable provenance from strategic goals to ground implementation."

**AI pitch**:
"Infrastructure for AI agents to understand purpose, not just syntax - every action knows why it exists."

**Research pitch**:
"A formal framework for hierarchical delegation with explicit provenance tracking and empirical strategy validation."

**Product pitch**:
"Turn your Git history into a queryable database of business decisions, searchable by purpose instead of just files."

---

## The Ultimate Demo Flow (7 Minutes)

### Minute 1: Hook
- "Your Git log answers 'what changed?' SixSpec makes it answer 'why?'"
- Show bad commit getting rejected by hook

### Minutes 2-3: Git Integration
- Write dimensional commit with WHY + HOW
- Hook accepts it
- Query history by purpose
- "Now Git is a knowledge base, not just a changelog"

### Minutes 4-5: Provenance Chain
- Show DiltsWalker execution
- Trace WHAT→WHY from mission to implementation
- "Every line of code knows why it exists"

### Minute 6: Power Features
- Hypergraph auto-organization OR
- Portfolio execution OR  
- A2A pause/resume
(Pick based on audience interest)

### Minute 7: Vision
- "Phase 1: Git commits (done)"
- "Phase 2: Full hierarchical delegation (done)"
- "Phase 3: Claude integration (next)"
- "Future: Agent ecosystems with traceable reasoning"

**End with**: "Want to try it on your codebase?" or "Should we explore Claude integration?"

