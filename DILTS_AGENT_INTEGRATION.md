# Agent Integration: Dilts Organizational Structure

## Vision

**Agents as Living Embodiment of Organizational Levels**

Each Dilts level can be represented by specialized agents that:
1. **Understand** the specifications at their level
2. **Execute** behaviors defined at their level
3. **Learn** by updating beliefs based on tactical feedback
4. **Communicate** across levels following purpose propagation

---

## Agent Positioning in the Dilts Hierarchy

### Core Principle: **Agents Operate at L2-BEHAVIORS**

Agents are positioned at **L2-BEHAVIORS** because this is where:
- **Strategy meets execution** (top-down approach)
- **Feedback meets learning** (bottom-up response)
- **Intent becomes action** (behaviors act on environment)
- **Reality informs strategy** (observations update beliefs)

```
L6: MISSION        → Strategic Direction
L5: IDENTITY       → Brand & Values
L4: BELIEFS        → Principles & Assumptions ← Agents UPDATE these
L3: CAPABILITIES   → Tools & Resources       ← Agents UTILIZE these
L2: BEHAVIORS      → WHERE AGENTS LIVE       ← Agents EXECUTE here
L1: ENVIRONMENT    → Context & Feedback      ← Agents OBSERVE this
```

---

## Agent Types by Function

### 1. **Strategic Agents** (Approach)
**Location**: `L2-BEHAVIORS/strategic/`  
**Function**: Execute top-down initiatives based on beliefs

```python
@dataclass
class StrategicAgent:
    """Agents that implement organizational strategy"""
    
    level: Literal["L2-BEHAVIORS/strategic"]
    role: str  # "market-entry", "product-launch", "resource-allocation"
    
    # Inputs from higher levels
    mission: str         # From L6
    identity: str        # From L5
    beliefs: List[str]   # From L4 (guiding assumptions)
    capabilities: List[str]  # From L3 (available tools)
    
    # Execution
    approach: str        # The strategic initiative
    confidence: float    # Confidence in strategy (0.60-0.85)
    
    # Tools
    allowed_tools: List[str]  # Claude tools: Read, Write, Bash, etc.
    mcp_servers: Dict[str, Any]  # Custom MCP servers
```

**Example**: Market Entry Agent

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition

# Define market entry agent
market_entry_agent = AgentDefinition(
    description="Execute market entry strategy for new enterprise segment",
    prompt=f"""
    You are the Market Entry Strategic Agent.
    
    MISSION (L6): {org.mission}
    IDENTITY (L5): {org.identity}
    BELIEFS (L4): {org.beliefs['market-assumptions']}
    CAPABILITIES (L3): {org.capabilities['devops-platform']}
    
    YOUR APPROACH:
    - Launch enterprise tier through channel partnerships
    - Target Fortune 500 companies
    - Execute quarterly rollout plan
    
    CONFIDENCE: 0.75 (planned initiative, not yet validated)
    
    Use available tools to execute strategy:
    - Research target companies
    - Draft partnership proposals
    - Create launch materials
    - Track progress metrics
    """,
    tools=["Read", "Write", "Grep", "WebSearch"],
    model="sonnet"
)

# Configure agent options
options = ClaudeAgentOptions(
    agents={"market_entry": market_entry_agent},
    allowed_tools=["Read", "Write", "Grep", "WebSearch"],
    permission_mode="acceptEdits",
    cwd="/home/Projects/org/L2-BEHAVIORS/strategic/"
)

# Execute strategic approach
async with ClaudeSDKClient(options=options) as client:
    await client.query("Execute the Q2 enterprise market entry strategy")
    
    async for message in client.receive_response():
        # Agent executes strategy, creates files, researches market
        print(message)
```

### 2. **Tactical Agents** (Response)
**Location**: `L2-BEHAVIORS/tactical/`  
**Function**: Observe environment feedback and inform strategic refinement

```python
@dataclass
class TacticalAgent:
    """Agents that process market feedback and update beliefs"""
    
    level: Literal["L2-BEHAVIORS/tactical"]
    role: str  # "market-response", "customer-feedback", "performance-monitor"
    
    # Inputs from environment
    observations: List[Dict]  # From L1 (market data, metrics, feedback)
    
    # Analysis
    response: str            # What we learned
    confidence: float        # Confidence in observations (0.85-1.0)
    
    # Outputs to higher levels
    capability_updates: List[str]   # Updates to L3
    belief_revisions: List[str]     # Updates to L4
    identity_refinements: List[str]  # Updates to L5 (rare)
    
    # Tools
    allowed_tools: List[str]  # Read, Grep, custom analytics tools
```

**Example**: Customer Feedback Agent

```python
# Define customer feedback tactical agent
feedback_agent = AgentDefinition(
    description="Analyze customer feedback and update organizational beliefs",
    prompt=f"""
    You are the Customer Feedback Tactical Agent.
    
    YOUR MISSION:
    Observe market responses and update organizational understanding.
    
    PROCESS:
    1. READ: Analyze customer feedback from L1-ENVIRONMENT/
       - Support tickets
       - Survey responses
       - Churn analysis
       - Usage metrics
    
    2. ANALYZE: Identify patterns and insights
       - What are customers actually experiencing?
       - What assumptions are validated/invalidated?
       - What capabilities need updating?
    
    3. UPDATE: Revise organizational knowledge
       - Move beliefs to validated/ or invalidated/
       - Update confidence scores based on evidence
       - Suggest capability additions
       - Document learnings
    
    CONFIDENCE: 0.95 (based on direct observations)
    
    OUTPUT FORMAT:
    - Updated .w5h1 files in L4-BELIEFS/
    - New files in L3-CAPABILITIES/ if needed
    - Detailed analysis reports
    """,
    tools=["Read", "Write", "Grep", "Edit"],
    model="sonnet"
)

options = ClaudeAgentOptions(
    agents={"feedback_analyzer": feedback_agent},
    allowed_tools=["Read", "Write", "Grep", "Edit"],
    cwd="/home/Projects/org/"
)

# Process market feedback
async with ClaudeSDKClient(options=options) as client:
    await client.query("""
    Analyze customer feedback from the Q2 enterprise launch.
    
    1. Read all feedback files in L1-ENVIRONMENT/market/feedback/
    2. Identify patterns (what worked, what didn't)
    3. Update relevant beliefs in L4-BELIEFS/assumptions/
    4. Suggest new capabilities if needed
    5. Generate summary report
    """)
    
    async for message in client.receive_response():
        # Agent analyzes feedback, updates beliefs, improves org knowledge
        print(message)
```

### 3. **Belief Validation Agents**
**Location**: `L4-BELIEFS/`  
**Function**: Validate/invalidate assumptions based on evidence

```python
belief_validator_agent = AgentDefinition(
    description="Validate organizational assumptions through systematic testing",
    prompt="""
    You are the Belief Validation Agent.
    
    YOUR ROLE:
    Systematically validate or invalidate organizational assumptions.
    
    PROCESS:
    1. IDENTIFY: Find beliefs needing validation
       - confidence < 0.70
       - status: "validation_needed"
       - no recent validation
    
    2. DESIGN: Create validation tests
       - A/B tests
       - User interviews
       - Market analysis
       - Performance metrics
    
    3. EXECUTE: Run validation experiments
       - Coordinate with strategic agents
       - Gather data from environment
       - Analyze results
    
    4. UPDATE: Move beliefs appropriately
       - validated/ if proven (confidence → 0.85+)
       - invalidated/ if disproven (document why)
       - Update evidence trail
    
    5. INFORM: Alert strategic agents
       - Validated beliefs → higher confidence strategies
       - Invalidated beliefs → strategic pivots needed
    """,
    tools=["Read", "Write", "Edit", "Grep", "Bash"],
    model="sonnet"
)

# Example: Validate pricing assumption
async with ClaudeSDKClient(options=options) as client:
    await client.query("""
    Validate the assumption in L4-BELIEFS/assumptions/market/pricing.w5h1
    
    Current: "Market will pay $50/month" (confidence: 0.60)
    
    1. Design A/B test with $35/$50 pricing
    2. Run test (coordinate with market-entry agent)
    3. Analyze conversion and churn data
    4. Update belief based on evidence
    5. If invalidated, suggest revised pricing belief
    """)
```

### 4. **Capability Enhancement Agents**
**Location**: `L3-CAPABILITIES/`  
**Function**: Identify and add new capabilities based on market needs

```python
capability_scout_agent = AgentDefinition(
    description="Identify new capabilities needed based on market feedback",
    prompt="""
    You are the Capability Scout Agent.
    
    YOUR ROLE:
    Identify gaps between current capabilities and market needs.
    
    INPUTS:
    - Tactical feedback from L2-BEHAVIORS/tactical/
    - Market observations from L1-ENVIRONMENT/
    - Current capabilities from L3-CAPABILITIES/
    
    PROCESS:
    1. ANALYZE: What do customers need that we don't offer?
    2. PRIORITIZE: Which capabilities have highest impact?
    3. SPECIFY: Create detailed .w5h1 capability specs
    4. VALIDATE: Check alignment with beliefs and identity
    5. RECOMMEND: Propose to strategic agents for implementation
    
    OUTPUT:
    New .w5h1 files in L3-CAPABILITIES/proposed/
    """,
    tools=["Read", "Write", "Grep", "WebSearch"],
    model="sonnet"
)
```

### 5. **Purpose Propagation Agents**
**Location**: Cross-level  
**Function**: Ensure parent WHAT → child WHY alignment

```python
purpose_validator_agent = AgentDefinition(
    description="Validate purpose propagation throughout organization",
    prompt="""
    You are the Purpose Propagation Validator.
    
    YOUR ROLE:
    Ensure every specification traces back to mission.
    
    VALIDATION:
    1. For each .w5h1 file, verify:
       - parent_spec is defined (except L6)
       - Child's WHY matches parent's WHAT
       - Confidence propagates appropriately
       - Purpose chain is unbroken to L6
    
    2. Generate reports:
       - Orphaned specs (missing parents)
       - Misaligned purposes
       - Broken chains
       - Confidence gaps
    
    3. Fix issues:
       - Update WHY dimensions to match parent WHAT
       - Add missing parent references
       - Document purpose chains
    
    OUTPUT:
    - Validation report
    - Fixed .w5h1 files
    - Purpose chain diagrams
    """,
    tools=["Read", "Write", "Edit", "Grep"],
    model="sonnet"
)
```

---

## Multi-Agent Orchestration

### The Learning Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                    STRATEGIC AGENTS                         │
│               (Execute top-down approach)                   │
│                                                             │
│  market_entry_agent → product_launch_agent → growth_agent  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Acts on Environment
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    L1: ENVIRONMENT                          │
│              (Market responds to actions)                   │
│                                                             │
│  Customer feedback, metrics, observations, market data      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Feedback flows up
                           ↑
┌─────────────────────────────────────────────────────────────┐
│                    TACTICAL AGENTS                          │
│             (Process feedback, learn, adapt)                │
│                                                             │
│  feedback_agent → metrics_agent → competitive_intel_agent   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Updates beliefs
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                 BELIEF VALIDATION AGENTS                    │
│            (Validate/invalidate assumptions)                │
│                                                             │
│  Move assumptions to validated/ or invalidated/             │
│  Update confidence scores with evidence                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Informs next strategy
                           ↓
                 (Cycle repeats with higher confidence)
```

### Orchestration Example

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition

async def full_learning_cycle():
    """
    Complete strategic cycle:
    1. Strategic agent executes approach
    2. Environment responds
    3. Tactical agent observes and learns
    4. Beliefs updated
    5. Next strategy more informed
    """
    
    # Define all agents
    strategic_agent = AgentDefinition(
        description="Execute market entry strategy",
        prompt="[Strategic agent prompt]",
        tools=["Read", "Write", "WebSearch"],
        model="sonnet"
    )
    
    tactical_agent = AgentDefinition(
        description="Analyze market response",
        prompt="[Tactical agent prompt]",
        tools=["Read", "Grep", "Edit"],
        model="sonnet"
    )
    
    validator_agent = AgentDefinition(
        description="Validate beliefs based on evidence",
        prompt="[Validator agent prompt]",
        tools=["Read", "Write", "Edit"],
        model="sonnet"
    )
    
    options = ClaudeAgentOptions(
        agents={
            "strategy": strategic_agent,
            "tactics": tactical_agent,
            "validator": validator_agent
        },
        allowed_tools=["Read", "Write", "Edit", "Grep", "WebSearch", "Bash"],
        cwd="/home/Projects/org/"
    )
    
    async with ClaudeSDKClient(options=options) as client:
        # STEP 1: Strategic approach
        print("=== STRATEGIC PHASE ===")
        await client.query("""
        @strategy: Execute Q2 market entry plan
        - Target: Fortune 500 companies
        - Approach: Channel partnerships
        - Timeline: 3 months
        """)
        
        async for message in client.receive_response():
            print(f"Strategy: {message}")
        
        # STEP 2: Wait for environment response (simulated)
        print("\n=== MARKET RESPONSE (simulated) ===")
        await asyncio.sleep(2)
        print("Market data collected in L1-ENVIRONMENT/")
        
        # STEP 3: Tactical response
        print("\n=== TACTICAL PHASE ===")
        await client.query("""
        @tactics: Analyze Q2 market entry results
        - Read feedback from L1-ENVIRONMENT/market/feedback/
        - Identify what worked vs. what didn't
        - Calculate metrics (conversion, retention, satisfaction)
        - Generate learnings report
        """)
        
        async for message in client.receive_response():
            print(f"Tactics: {message}")
        
        # STEP 4: Belief validation
        print("\n=== VALIDATION PHASE ===")
        await client.query("""
        @validator: Update beliefs based on Q2 results
        - Review tactical analysis
        - Update relevant beliefs in L4-BELIEFS/
        - Move assumptions to validated/invalidated/
        - Adjust confidence scores
        - Generate updated belief report
        """)
        
        async for message in client.receive_response():
            print(f"Validator: {message}")
        
        # STEP 5: Next cycle with updated beliefs
        print("\n=== NEXT STRATEGIC PHASE (informed) ===")
        await client.query("""
        @strategy: Plan Q3 market entry (informed by Q2 learnings)
        - Read validated beliefs from L4-BELIEFS/validated/
        - Use higher confidence assumptions
        - Adjust approach based on Q2 learnings
        - Execute with refined strategy
        """)
        
        async for message in client.receive_response():
            print(f"Refined Strategy: {message}")

# Run the full cycle
asyncio.run(full_learning_cycle())
```

---

## Agent Hooks for Organizational Learning

### Hook 1: Pre-Tool Belief Check

```python
async def belief_confidence_check(
    input_data: dict,
    tool_use_id: str | None,
    context: HookContext
) -> dict:
    """
    Before executing tools, check if related beliefs have sufficient confidence.
    Warn if strategy is based on low-confidence assumptions.
    """
    tool_name = input_data.get('tool_name')
    
    # If agent is making strategic decisions
    if tool_name in ["Write", "Edit"] and "strategic" in input_data.get('file_path', ''):
        # Load related beliefs
        beliefs = load_relevant_beliefs(input_data)
        
        low_confidence = [b for b in beliefs if b.confidence < 0.70]
        
        if low_confidence:
            return {
                'systemMessage': f"""
                WARNING: Strategy based on low-confidence beliefs:
                {', '.join([f"{b.name} ({b.confidence})" for b in low_confidence])}
                
                Consider validating these assumptions before proceeding.
                """
            }
    
    return {}
```

### Hook 2: Post-Tool Learning Capture

```python
async def capture_learnings(
    input_data: dict,
    tool_use_id: str | None,
    context: HookContext
) -> dict:
    """
    After tool execution, capture learnings for future reference.
    Automatically update tactical knowledge base.
    """
    tool_name = input_data.get('tool_name')
    
    # If tool execution provides market feedback
    if tool_name in ["Read", "Grep", "WebSearch"]:
        result = input_data.get('tool_result', {})
        
        # Extract insights
        insights = extract_insights(result)
        
        if insights:
            # Automatically create tactical report
            create_tactical_report(insights)
            
            return {
                'systemMessage': f"""
                Tactical insight captured: {insights['summary']}
                Report saved to L2-BEHAVIORS/tactical/auto-generated/
                Relevant beliefs flagged for review.
                """
            }
    
    return {}
```

### Hook 3: Purpose Propagation Validator

```python
async def validate_purpose_chain(
    input_data: dict,
    tool_use_id: str | None,
    context: HookContext
) -> dict:
    """
    When creating/editing .w5h1 files, validate purpose propagation.
    """
    tool_name = input_data.get('tool_name')
    
    if tool_name in ["Write", "Edit"] and '.w5h1' in input_data.get('file_path', ''):
        file_path = input_data['file_path']
        content = input_data.get('content', '')
        
        # Parse W5H1 content
        spec = parse_w5h1(content)
        
        # Check purpose propagation
        if spec.parent_spec:
            parent = load_w5h1(spec.parent_spec)
            
            if spec.why != parent.what:
                return {
                    'decision': 'block',
                    'systemMessage': f"""
                    PURPOSE PROPAGATION ERROR:
                    
                    Parent WHAT: {parent.what}
                    Child WHY:   {spec.why}
                    
                    These must match! Please update child's WHY to match parent's WHAT.
                    """
                }
    
    return {}
```

---

## Agent Directory Structure

```
/home/Projects/org/
├── .agents/
│   ├── strategic/
│   │   ├── market-entry-agent.py
│   │   ├── product-launch-agent.py
│   │   └── growth-agent.py
│   │
│   ├── tactical/
│   │   ├── feedback-analyzer-agent.py
│   │   ├── metrics-monitor-agent.py
│   │   └── competitive-intel-agent.py
│   │
│   ├── validators/
│   │   ├── belief-validator-agent.py
│   │   ├── purpose-propagation-agent.py
│   │   └── confidence-tracker-agent.py
│   │
│   └── orchestration/
│       ├── learning-cycle-orchestrator.py
│       ├── multi-agent-coordinator.py
│       └── agent-registry.json
│
├── L6-MISSION/
├── L5-IDENTITY/
├── L4-BELIEFS/
│   └── (agents UPDATE these based on tactical feedback)
│
├── L3-CAPABILITIES/
│   └── (agents UTILIZE these as tools)
│
├── L2-BEHAVIORS/
│   ├── strategic/
│   │   └── (STRATEGIC AGENTS execute here)
│   └── tactical/
│       └── (TACTICAL AGENTS analyze here)
│
└── L1-ENVIRONMENT/
    └── (agents OBSERVE this for feedback)
```

---

## Implementation Roadmap

### Phase 1: Single Strategic Agent (Week 1)
- [ ] Create one strategic agent for market analysis
- [ ] Configure with Read, Write, WebSearch tools
- [ ] Execute simple strategy (research competitors)
- [ ] Output to L2-BEHAVIORS/strategic/

### Phase 2: Tactical Feedback Agent (Week 2)
- [ ] Create tactical agent to analyze results
- [ ] Read from L1-ENVIRONMENT/
- [ ] Generate insights report
- [ ] Output to L2-BEHAVIORS/tactical/

### Phase 3: Belief Validator Agent (Week 3)
- [ ] Create validator agent
- [ ] Validate/invalidate assumptions
- [ ] Move beliefs to validated/invalidated/
- [ ] Update confidence scores

### Phase 4: Multi-Agent Orchestration (Week 4)
- [ ] Orchestrator coordinates agents
- [ ] Full learning cycle automation
- [ ] Agent-to-agent communication
- [ ] Progress tracking and reporting

### Phase 5: Advanced Features (Weeks 5-6)
- [ ] Hooks for automatic learning capture
- [ ] Purpose propagation validation
- [ ] Confidence-based decision making
- [ ] Agent performance metrics

---

## Key Benefits

### 1. **Automated Organizational Learning**
Agents continuously:
- Execute strategies (strategic agents)
- Observe results (tactical agents)
- Update beliefs (validator agents)
- Improve over time (learning loop)

### 2. **Explicit Knowledge Management**
All agent actions are:
- Documented in .w5h1 files
- Traceable through git history
- Queryable through org_query_example.py
- Auditable for compliance

### 3. **Confidence-Driven Decisions**
Agents respect confidence scores:
- Low confidence → validate before acting
- High confidence → execute boldly
- Evidence-based → adjust confidence continuously

### 4. **Purpose-Aligned Execution**
Every agent action:
- Traces back to mission (L6)
- Aligns with identity (L5)
- Follows beliefs (L4)
- Utilizes capabilities (L3)
- Executes at behaviors (L2)
- Observes environment (L1)

---

## Summary

**Agents Position**: **L2-BEHAVIORS** (the pivot point)

**Agent Types**:
1. **Strategic** (approach) - Execute top-down initiatives
2. **Tactical** (response) - Process bottom-up feedback
3. **Validators** - Validate/invalidate beliefs
4. **Scouts** - Identify new capabilities
5. **Propagators** - Ensure purpose alignment

**The Result**: Self-improving organization where:
- Strategy is tested continuously
- Feedback updates beliefs automatically
- Confidence increases with evidence
- Purpose remains aligned
- Learning is captured systematically

**Your organization becomes a learning system powered by agents.** 🤖
