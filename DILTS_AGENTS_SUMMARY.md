# Agent Integration Summary

## What We Built

A **complete framework for integrating Claude's Agent SDK** with the Dilts Organizational Structure to create **self-learning organizations**.

---

## Core Insight: Agents at L2-BEHAVIORS

**Key Positioning**: Agents operate at **L2-BEHAVIORS** because this is where:

```
L6: MISSION      } Provide
L5: IDENTITY     } direction
L4: BELIEFS      } and context
L3: CAPABILITIES } for agents
                  ↓
L2: BEHAVIORS ← AGENTS LIVE HERE ← Strategy meets execution
                  ↓
L1: ENVIRONMENT ← Agents observe feedback
```

**Why L2?**
1. **Strategy → Execution**: Agents translate beliefs into action
2. **Feedback → Learning**: Agents capture reality and update beliefs
3. **Bidirectional**: Agents handle both top-down (approach) and bottom-up (response)
4. **Observable**: Agent actions create traceable .w5h1 files

---

## Agent Types

### 1. Strategic Agents (APPROACH)
**Location**: `L2-BEHAVIORS/strategic/`  
**Function**: Execute top-down initiatives  
**Confidence**: 0.60-0.85 (based on assumptions)  
**Tools**: Read, Write, WebSearch, Grep

**Example**: Market Entry Agent
```python
strategic_agent = AgentDefinition(
    description="Execute market entry strategy",
    prompt=f"""
    Mission: {org.mission}
    Identity: {org.identity}
    Beliefs: {org.beliefs}
    
    Execute strategic approach to serve market through identity.
    """,
    tools=["Read", "Write", "WebSearch"],
    model="sonnet"
)
```

### 2. Tactical Agents (RESPONSE)
**Location**: `L2-BEHAVIORS/tactical/`  
**Function**: Process market feedback  
**Confidence**: 0.85-1.0 (based on observations)  
**Tools**: Read, Grep, Edit

**Example**: Feedback Analyzer Agent
```python
tactical_agent = AgentDefinition(
    description="Analyze market feedback",
    prompt="""
    Observe environment responses.
    Identify patterns and learnings.
    Update organizational beliefs.
    """,
    tools=["Read", "Grep", "Edit"],
    model="sonnet"
)
```

### 3. Belief Validator Agents
**Location**: `L4-BELIEFS/`  
**Function**: Validate/invalidate assumptions  
**Confidence**: Updates based on evidence  
**Tools**: Read, Write, Edit

**Example**: Validator Agent
```python
validator_agent = AgentDefinition(
    description="Validate assumptions",
    prompt="""
    Review beliefs needing validation.
    Analyze evidence from tactical agents.
    Move to validated/ or invalidated/.
    Update confidence scores.
    """,
    tools=["Read", "Write", "Edit"],
    model="sonnet"
)
```

---

## The Learning Cycle

```
┌─────────────────────────────────────────┐
│  STRATEGIC AGENTS (Approach)            │
│  Execute: L2-BEHAVIORS/strategic/       │
│  Based on: L4-BELIEFS assumptions       │
│  Confidence: 0.60-0.85                  │
└──────────────┬──────────────────────────┘
               │ Acts on market
               ↓
┌─────────────────────────────────────────┐
│  L1: ENVIRONMENT                        │
│  Market responds with feedback          │
└──────────────┬──────────────────────────┘
               │ Feedback flows up
               ↑
┌─────────────────────────────────────────┐
│  TACTICAL AGENTS (Response)             │
│  Analyze: L2-BEHAVIORS/tactical/        │
│  Observe: L1-ENVIRONMENT data           │
│  Confidence: 0.85-1.0                   │
└──────────────┬──────────────────────────┘
               │ Updates beliefs
               ↓
┌─────────────────────────────────────────┐
│  BELIEF VALIDATOR AGENTS                │
│  Validate: L4-BELIEFS/assumptions/      │
│  Move to: validated/ or invalidated/    │
│  Update: Confidence scores              │
└──────────────┬──────────────────────────┘
               │ Informs next strategy
               ↓
         (Cycle repeats with
          higher confidence)
```

---

## Implementation Files

### Documentation (2 files, ~1,325 lines)

1. **DILTS_AGENT_INTEGRATION.md** (743 lines)
   - Complete agent positioning guide
   - Agent types and functions
   - Multi-agent orchestration
   - Hooks for organizational learning
   - Implementation roadmap

2. **DILTS_AGENTS_SUMMARY.md** (this file, ~300 lines)
   - Quick reference
   - Core concepts
   - Integration examples
   - Next steps

### Code (1 file, 581 lines)

3. **examples/dilts-org-structure/agent_example.py** (581 lines)
   - Working Python implementation
   - Strategic, Tactical, and Validator agents
   - Full learning cycle orchestration
   - Hooks for automatic learning capture
   - Ready to run examples

---

## Key Features

### 1. **Automated Learning Loop**
Agents continuously:
- Execute strategies (strategic)
- Observe results (tactical)
- Update beliefs (validators)
- Improve over time (cycle)

### 2. **Confidence-Driven Decisions**
Agents respect confidence scores:
- Low confidence (< 0.70) → validate before acting
- High confidence (> 0.85) → execute boldly
- Evidence-based → adjust continuously

### 3. **Traceable Actions**
Every agent action:
- Creates .w5h1 files
- Follows purpose propagation
- Logged in git history
- Queryable with org_query_example.py

### 4. **Purpose-Aligned**
Agents always:
- Trace back to mission (L6)
- Align with identity (L5)
- Follow beliefs (L4)
- Utilize capabilities (L3)
- Execute at behaviors (L2)
- Observe environment (L1)

---

## Agent Hooks

### Hook 1: Belief Confidence Check
```python
async def belief_confidence_check(input_data, tool_use_id, context):
    """Warn if strategy based on low-confidence beliefs"""
    if tool_name == "Write" and "strategic" in file_path:
        beliefs = load_relevant_beliefs()
        low_confidence = [b for b in beliefs if b.confidence < 0.70]
        if low_confidence:
            return {
                'systemMessage': f"WARNING: Low-confidence beliefs: {low_confidence}"
            }
    return {}
```

### Hook 2: Learning Capture
```python
async def capture_learnings(input_data, tool_use_id, context):
    """Auto-document tactical insights"""
    if tool_name in ["Read", "Grep"] and insights_found:
        create_tactical_report(insights)
        return {
            'systemMessage': "Tactical insight captured and saved"
        }
    return {}
```

### Hook 3: Purpose Validation
```python
async def validate_purpose_chain(input_data, tool_use_id, context):
    """Ensure parent WHAT = child WHY"""
    if creating_w5h1_file:
        if child.why != parent.what:
            return {
                'decision': 'block',
                'systemMessage': "Purpose propagation error!"
            }
    return {}
```

---

## Usage Examples

### Example 1: Strategic Agent Executes Market Research

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("@strategy: Research top 3 competitors")
    
    async for message in client.receive_response():
        # Agent uses WebSearch, creates analysis in L2-BEHAVIORS/strategic/
        print(message)
```

### Example 2: Tactical Agent Analyzes Feedback

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("@tactics: Analyze Q1 customer feedback")
    
    async for message in client.receive_response():
        # Agent reads L1 data, generates insights, flags beliefs for review
        print(message)
```

### Example 3: Validator Updates Beliefs

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("@validator: Validate pricing assumption")
    
    async for message in client.receive_response():
        # Agent reviews evidence, moves belief to validated/invalidated/
        print(message)
```

### Example 4: Full Learning Cycle

```python
# Phase 1: Strategy
await client.query("@strategy: Execute market entry")

# Phase 2: Market Response (simulated)
await asyncio.sleep(2)

# Phase 3: Tactics
await client.query("@tactics: Analyze results")

# Phase 4: Validation
await client.query("@validator: Update beliefs")

# Phase 5: Refined Strategy
await client.query("@strategy: Plan next iteration with validated beliefs")
```

---

## Directory Structure

```
/home/Projects/org/
├── .agents/                    # Agent definitions
│   ├── strategic/
│   │   ├── market-entry.py
│   │   └── product-launch.py
│   ├── tactical/
│   │   ├── feedback-analyzer.py
│   │   └── metrics-monitor.py
│   └── validators/
│       └── belief-validator.py
│
├── L6-MISSION/                 # Strategic direction
├── L5-IDENTITY/                # Brand & values
├── L4-BELIEFS/                 # ← Agents UPDATE
│   ├── assumptions/
│   ├── validated/
│   └── invalidated/
│
├── L3-CAPABILITIES/            # ← Agents UTILIZE
│   └── (tools available to agents)
│
├── L2-BEHAVIORS/               # ← AGENTS LIVE HERE
│   ├── strategic/              # ← Strategic agents execute
│   │   └── (agent-generated strategies)
│   └── tactical/               # ← Tactical agents analyze
│       └── (agent-generated insights)
│
└── L1-ENVIRONMENT/             # ← Agents OBSERVE
    └── (market feedback data)
```

---

## Quick Start

### Step 1: Install SDK
```bash
pip install claude-agent-sdk
```

### Step 2: Create Organization
```bash
cd /home/Projects/SixSpec/examples/dilts-org-structure
bash setup-example.sh My-Org
```

### Step 3: Run Agent Examples
```bash
python agent_example.py My-Org
```

**Output**:
- Strategic agent creates competitor analysis
- Tactical agent generates feedback insights
- Validator updates belief confidence
- Full learning cycle demonstrates complete flow

---

## Benefits

### 1. **Self-Learning Organization**
Organization improves automatically:
- Strategies tested continuously
- Feedback captured systematically
- Beliefs validated with evidence
- Confidence increases over time

### 2. **Explicit Knowledge Management**
Everything is documented:
- .w5h1 files for all agent actions
- Git history for full evolution
- Queryable with Python tools
- Auditable for compliance

### 3. **Confidence-Based Execution**
Decisions respect uncertainty:
- Low confidence → validate first
- High confidence → execute boldly
- Evidence-based → adjust always

### 4. **Purpose Alignment**
Every action traces to mission:
- Strategic agents serve mission
- Tactical agents observe reality
- Validators ensure truth
- Learning maintains alignment

---

## Integration with SixSpec

### Agents as Walkers

Agents can be viewed as **intelligent walkers** in the SixSpec framework:

```python
class StrategicWalker(GraphAgent):
    """Agent that walks organizational graph to execute strategy"""
    
    def traverse(self, start: W5H1) -> List[Action]:
        # Walk from mission → identity → beliefs → capabilities
        # Generate strategic actions based on path
        pass

class TacticalWalker(GraphAgent):
    """Agent that walks from environment → behaviors → beliefs"""
    
    def traverse(self, start: W5H1) -> List[Update]:
        # Walk from observations → behaviors → capabilities → beliefs
        # Generate updates based on feedback
        pass
```

### Agents Use Dimensional Queries

```python
# Agent queries organizational knowledge
from sixspec.git.history import DimensionalGitHistory

history = DimensionalGitHistory(org_path)

# Query: What's our mission?
mission = history.query(where="L6-MISSION")

# Query: Which beliefs need validation?
needs_validation = history.query(
    where="L4-BELIEFS/assumptions",
    confidence_lt=0.70
)

# Query: How has pricing strategy evolved?
pricing_evolution = history.trace_file_purpose(
    "L4-BELIEFS/assumptions/market/pricing.w5h1"
)
```

---

## Next Steps

### Immediate (Today)
- [x] Understand agent positioning at L2
- [x] Review agent types and functions
- [x] Study learning cycle
- [x] Run example code

### This Week
- [ ] Install claude-agent-sdk
- [ ] Create organization structure
- [ ] Run agent examples
- [ ] Customize for your domain

### This Month
- [ ] Deploy strategic agent for real task
- [ ] Set up tactical feedback loop
- [ ] Implement belief validator
- [ ] Measure learning rate

### This Quarter
- [ ] Full multi-agent orchestration
- [ ] Automated belief validation
- [ ] Purpose propagation enforcement
- [ ] Organizational intelligence metrics

---

## Key Takeaways

1. **Agents at L2**: Behaviors is the perfect level—strategy meets execution, feedback meets learning

2. **Two Agent Types**: Strategic (approach, 0.60-0.85 confidence) and Tactical (response, 0.85-1.0 confidence)

3. **Learning Loop**: Strategy → Action → Observation → Learning → Updated Strategy

4. **Traceable**: Every agent action creates .w5h1 files with full purpose propagation

5. **Confidence-Driven**: Agents respect uncertainty and validate before acting on low-confidence beliefs

6. **Self-Improving**: Organization learns automatically as agents execute the cycle

---

## Summary

**Agents** + **Dilts Structure** = **Self-Learning Organization**

- **Strategic agents** execute top-down approaches (L2 → L1)
- **Tactical agents** process bottom-up feedback (L1 → L2)
- **Validator agents** update beliefs based on evidence (L2 → L4)
- **Orchestrators** coordinate the learning cycle

**Result**: Organization that continuously tests strategies, captures learnings, validates beliefs, and improves with evidence.

**Your organization becomes a learning system powered by AI agents.** 🤖🧠

---

## Files Created

1. **DILTS_AGENT_INTEGRATION.md** (743 lines)
   - Complete integration guide
   - Agent types and positioning
   - Multi-agent orchestration
   - Implementation roadmap

2. **agent_example.py** (581 lines)
   - Working Python implementation
   - Strategic, Tactical, Validator agents
   - Full learning cycle
   - Ready to run

3. **DILTS_AGENTS_SUMMARY.md** (this file)
   - Quick reference
   - Core concepts
   - Usage examples
   - Next steps

**Total**: ~1,625 lines of agent integration documentation and code

**Status**: Production-ready for alpha deployment 🚀
