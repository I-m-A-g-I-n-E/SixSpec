# Implementation Outlines: Dilts Agent Integration

## Overview

These outlines define the work needed to integrate Claude Agent SDK with the Dilts organizational structure, implementing:
1. Middle Management Layer (L4 as provisioner)
2. Agent Dilts Structure (fractal pattern)
3. Lazy-loaded agent introspection
4. Shared budget system
5. Self-learning organizational loop

Each outline is designed to become a Linear issue with clear acceptance criteria.

---

## PHASE 1: FOUNDATION

### Issue 1.1: Implement L4 Middle Management - Permission Matrix

**Epic**: Middle Management Layer (Agent Provisioning)

**Description**:
Create the L4-BELIEFS permission matrix that provisions agents with tools based on belief confidence levels. This is the foundation of the middle management layer that controls agent capabilities.

**Background**:
- Agents need tools to execute tasks
- Tool access should correlate with confidence in underlying beliefs
- Low confidence → restricted access (safety)
- High confidence → expanded access (efficiency)

**Acceptance Criteria**:
- [ ] Create `L4-BELIEFS/permissions/agent-provisioning.w5h1` specification
- [ ] Define permission levels (restricted_sandbox, read_only, read_and_search, full_access)
- [ ] Map confidence ranges to permission levels:
  - confidence < 0.60 → restricted_sandbox (Read only)
  - confidence 0.60-0.70 → read_only (Read, Grep)
  - confidence 0.70-0.85 → read_and_search (Read, Grep, WebSearch)
  - confidence > 0.85 → full_access (Read, Write, Edit, WebSearch, Bash)
- [ ] Create permission matrix data structure in Python
- [ ] Unit tests for permission level determination

**Implementation Details**:
```python
# sixspec/agents/middle_management.py

@dataclass
class PermissionLevel:
    name: str
    tools: List[str]
    mcp_servers: List[str]
    confidence_min: float
    confidence_max: float

class MiddleManagement:
    def get_permission_level(self, belief_confidence: float) -> PermissionLevel:
        """Return appropriate permission level based on confidence"""
        pass
```

**Dependencies**: None

**Estimated Effort**: 3-5 hours

**Files to Create**:
- `L4-BELIEFS/permissions/agent-provisioning.w5h1`
- `sixspec/agents/middle_management.py`
- `tests/agents/test_middle_management.py`

---

### Issue 1.2: Implement Tool Request Workflow

**Epic**: Middle Management Layer (Agent Provisioning)

**Description**:
Create the workflow for agents to request additional tools from L4 middle management when they identify capability gaps. Includes approval logic based on alignment and confidence.

**Background**:
- Agents may need tools not initially granted
- Requests should be evaluated against org beliefs and mission alignment
- Some requests auto-approved, others escalate to human

**Acceptance Criteria**:
- [ ] Create `L4-BELIEFS/permissions/tool-request-workflow.w5h1` specification
- [ ] Implement ToolRequest data structure
- [ ] Implement approval logic:
  - Alignment score > 0.80 + tool available + confidence > 0.70 → auto-approve
  - Alignment score > 0.60 → escalate to human
  - Otherwise → deny with explanation
- [ ] Create MCP tool: `request_additional_tool`
- [ ] Log all tool requests (approved, denied, escalated)
- [ ] Unit tests for approval scenarios

**Implementation Details**:
```python
@dataclass
class ToolRequest:
    agent_id: str
    tool_name: str
    justification: str
    confidence_in_need: float
    current_mission: str

class MiddleManagement:
    def evaluate_tool_request(self, request: ToolRequest) -> ToolRequestResult:
        """Evaluate and approve/deny/escalate tool request"""
        alignment = self.calculate_alignment(request)
        if alignment > 0.80 and request.confidence_in_need > 0.70:
            return ToolRequestResult(approved=True)
        elif alignment > 0.60:
            return ToolRequestResult(escalate=True, reason="needs_human_review")
        else:
            return ToolRequestResult(approved=False, reason="misalignment")
```

**MCP Tool**:
```python
@tool("request_additional_tool", 
      "Request additional tool access from middle management", 
      {"tool_name": str, "justification": str, "confidence": float})
async def request_additional_tool(args: dict) -> dict:
    # Submit to middle management
    # Return approval status
    pass
```

**Dependencies**: Issue 1.1 (Permission Matrix)

**Estimated Effort**: 5-8 hours

**Files to Create**:
- `L4-BELIEFS/permissions/tool-request-workflow.w5h1`
- `sixspec/agents/tool_request.py`
- `sixspec/mcp/tools/request_additional_tool.py`
- `tests/agents/test_tool_request.py`

---

### Issue 1.3: Implement Shared Budget System

**Epic**: Resource Management

**Description**:
Create shared budget system where parent agents and their subagents draw from a common resource pool. Prevents runaway spawning and models real resource constraints.

**Background**:
- Agents can spawn subagents, creating resource consumption chains
- Need to prevent infinite recursion and resource exhaustion
- Budget can be tokens, API calls, or monetary cost
- Shared pool means parent allocation reduces child availability

**Acceptance Criteria**:
- [ ] Define budget unit (recommendation: API tokens)
- [ ] Create AgentBudget class with shared pool semantics
- [ ] Implement budget allocation for subagent spawning
- [ ] Implement budget request workflow
- [ ] Create MCP tool: `check_remaining_budget`
- [ ] Create MCP tool: `request_budget_increase`
- [ ] Depletion handling (what happens at budget=0)
- [ ] Budget tracking and reporting
- [ ] Unit tests for budget sharing and depletion

**Implementation Details**:
```python
@dataclass
class AgentBudget:
    total: int  # Total tokens allocated
    used: int   # Tokens consumed
    reserved: int  # Tokens allocated to subagents
    
    @property
    def available(self) -> int:
        return self.total - self.used - self.reserved
    
    def allocate_to_subagent(self, amount: int) -> bool:
        """Allocate budget slice to subagent (shared pool)"""
        if amount <= self.available:
            self.reserved += amount
            return True
        return False
    
    def consume(self, amount: int) -> bool:
        """Consume budget for agent action"""
        if amount <= self.available:
            self.used += amount
            return True
        return False
    
    def release_from_subagent(self, amount: int):
        """Return unused budget from completed subagent"""
        self.reserved -= amount

class BudgetManager:
    def create_budget(self, parent_budget: Optional[AgentBudget], 
                     requested_amount: int) -> AgentBudget:
        """Create budget for new agent, either root or from parent"""
        if parent_budget:
            if parent_budget.allocate_to_subagent(requested_amount):
                return AgentBudget(total=requested_amount, used=0, reserved=0)
            raise InsufficientBudgetError()
        else:
            # Root agent gets org-level budget
            return AgentBudget(total=requested_amount, used=0, reserved=0)
```

**MCP Tools**:
```python
@tool("check_remaining_budget", "Check your remaining budget", {})
async def check_remaining_budget(args: dict) -> dict:
    budget = get_current_agent_budget()
    return {"content": [{
        "type": "text",
        "text": f"Available: {budget.available} | Used: {budget.used} | Reserved: {budget.reserved}"
    }]}

@tool("request_budget_increase", 
      "Request additional budget from middle management",
      {"amount": int, "justification": str})
async def request_budget_increase(args: dict) -> dict:
    # Submit to L4 middle management for approval
    pass
```

**Dependencies**: Issue 1.2 (Tool Request Workflow - similar approval logic)

**Estimated Effort**: 8-10 hours

**Files to Create**:
- `sixspec/agents/budget.py`
- `sixspec/mcp/tools/budget_tools.py`
- `tests/agents/test_budget.py`
- `L4-BELIEFS/permissions/budget-allocation.w5h1`

---

## PHASE 2: AGENT STRUCTURE

### Issue 2.1: Implement Agent Dilts Structure (Lazy-Loaded)

**Epic**: Agent Internal Structure

**Description**:
Create the fractal Dilts structure for individual agents where each agent has its own L6-L1 levels, but these are lazy-loaded only when the agent queries them via tools.

**Background**:
- Agents should have their own Dilts logical levels
- L6 (Mission) inherited from org's WHAT at spawn level
- L5 (Identity) defined by system prompt
- L3 (Capabilities) = granted tools/permissions
- Lazy loading for performance (only load when queried)

**Acceptance Criteria**:
- [ ] Create AgentDilts class with lazy properties
- [ ] Implement lazy loading mechanism (load on first access)
- [ ] Create MCP tool: `query_self_dilts` for agent introspection
- [ ] Define storage location for agent Dilts data:
  - `.agents/instances/{agent_id}/dilts/`
- [ ] Purpose propagation: org WHAT → agent L6 mission
- [ ] Identity generation from system prompt → agent L5
- [ ] Capability mapping: granted tools → agent L3
- [ ] Unit tests for lazy loading behavior
- [ ] Integration test: agent queries own mission

**Implementation Details**:
```python
class AgentDilts:
    """Lazy-loaded Dilts structure for individual agent"""
    
    def __init__(self, agent_id: str, org_context: Dict, spawn_level: str):
        self.agent_id = agent_id
        self.org_context = org_context
        self.spawn_level = spawn_level
        self._cache = {}  # Lazy load cache
    
    @property
    def mission(self) -> Dict:
        """L6: Lazy load agent mission (inherited from org WHAT)"""
        if 'L6' not in self._cache:
            self._cache['L6'] = self._load_mission()
        return self._cache['L6']
    
    @property
    def identity(self) -> Dict:
        """L5: Lazy load agent identity (from system prompt)"""
        if 'L5' not in self._cache:
            self._cache['L5'] = self._load_identity()
        return self._cache['L5']
    
    @property
    def capabilities(self) -> Dict:
        """L3: Lazy load granted capabilities (tools/permissions)"""
        if 'L3' not in self._cache:
            self._cache['L3'] = self._load_capabilities()
        return self._cache['L3']
    
    def _load_mission(self) -> Dict:
        """Load from org WHAT at spawn level"""
        org_spec = load_org_spec(self.org_context, self.spawn_level)
        return {
            'what': org_spec.dimensions.get('WHAT'),
            'inherited_from': f'{self.spawn_level}/WHAT',
            'confidence': org_spec.get_confidence('WHAT')
        }
    
    def query_level(self, level: str) -> Dict:
        """Explicit query interface for tool use"""
        level_map = {
            'L6': self.mission,
            'L5': self.identity,
            'L3': self.capabilities
        }
        return level_map.get(level, {})
```

**MCP Tool**:
```python
@tool("query_self_dilts", 
      "Query your own Dilts structure (mission, identity, capabilities)",
      {"level": str})  # L6, L5, L4, L3, L2, L1
async def query_self_dilts(args: dict) -> dict:
    agent_dilts = get_current_agent_dilts()
    level_data = agent_dilts.query_level(args['level'])
    
    return {"content": [{
        "type": "text",
        "text": yaml.dump(level_data, default_flow_style=False)
    }]}
```

**Dependencies**: None

**Estimated Effort**: 10-12 hours

**Files to Create**:
- `sixspec/agents/agent_dilts.py`
- `sixspec/mcp/tools/query_self_dilts.py`
- `.agents/templates/agent-dilts-template.yaml`
- `tests/agents/test_agent_dilts.py`

---

### Issue 2.2: Implement Agent Instance Management

**Epic**: Agent Internal Structure

**Description**:
Create agent instance tracking system with registry, lifecycle management, and storage for agent-specific data including lazy-loaded Dilts structures.

**Background**:
- Multiple agents may be active simultaneously
- Each agent needs unique ID and storage
- Need to track agent lifecycle (spawned, active, completed, failed)
- Agent data persists for audit trail

**Acceptance Criteria**:
- [ ] Create agent registry at `.agents/registry.json`
- [ ] Implement AgentInstance class with lifecycle states
- [ ] Create instance storage directory structure:
  ```
  .agents/instances/{agent_id}/
  ├── dilts/           # Lazy-loaded Dilts levels
  ├── logs/            # Action logs
  ├── budget.json      # Budget tracking
  └── metadata.json    # Spawn context, parent, etc.
  ```
- [ ] Implement spawn tracking (parent-child relationships)
- [ ] Implement cleanup for completed agents (archive vs. delete)
- [ ] Query interface: list active agents, get agent details
- [ ] Unit tests for lifecycle management

**Implementation Details**:
```python
@dataclass
class AgentInstance:
    agent_id: str
    agent_type: str  # "strategic", "tactical", "validator"
    spawn_level: str  # Which org level spawned this
    parent_agent_id: Optional[str]
    status: str  # "active", "completed", "failed", "paused"
    budget: AgentBudget
    dilts: AgentDilts  # Lazy-loaded structure
    created_at: datetime
    completed_at: Optional[datetime]

class AgentRegistry:
    def register_agent(self, instance: AgentInstance) -> str:
        """Add agent to registry, return agent_id"""
        pass
    
    def get_agent(self, agent_id: str) -> Optional[AgentInstance]:
        """Retrieve agent instance"""
        pass
    
    def list_active_agents(self) -> List[AgentInstance]:
        """List all active agents"""
        pass
    
    def update_status(self, agent_id: str, status: str):
        """Update agent lifecycle status"""
        pass
    
    def cleanup_completed_agents(self, archive: bool = True):
        """Clean up completed agents"""
        pass
```

**Dependencies**: Issue 2.1 (Agent Dilts Structure)

**Estimated Effort**: 8-10 hours

**Files to Create**:
- `sixspec/agents/registry.py`
- `sixspec/agents/instance.py`
- `.agents/registry.json` (template)
- `tests/agents/test_registry.py`

---

### Issue 2.3: Implement Budget Tracking and Consumption

**Epic**: Resource Management

**Description**:
Implement actual budget tracking during agent execution, including consumption on tool use, allocation to subagents, and budget exhaustion handling.

**Background**:
- Agents consume budget with each tool call
- Subagents draw from parent's shared pool
- Need real-time tracking and warnings
- Must handle budget exhaustion gracefully

**Acceptance Criteria**:
- [ ] Hook into tool execution to track consumption
- [ ] Define cost per tool type (e.g., Read=10 tokens, Write=50, Bash=100, WebSearch=200)
- [ ] Implement budget deduction on tool use
- [ ] Implement budget allocation for subagent spawning
- [ ] Budget release when subagent completes
- [ ] Warning at 80% budget consumed
- [ ] Graceful handling at 100% (pause agent, request more, or fail)
- [ ] Budget reporting: total, used, reserved, available
- [ ] Integration test: spawn subagent, consume budget, verify sharing

**Implementation Details**:
```python
TOOL_COSTS = {
    "Read": 10,
    "Write": 50,
    "Edit": 40,
    "Grep": 15,
    "WebSearch": 200,
    "Bash": 100,
}

class BudgetTracker:
    def track_tool_use(self, agent_id: str, tool_name: str) -> bool:
        """Deduct budget for tool use, return True if sufficient"""
        agent = registry.get_agent(agent_id)
        cost = TOOL_COSTS.get(tool_name, 10)
        
        if agent.budget.consume(cost):
            self.log_consumption(agent_id, tool_name, cost)
            
            # Warn if low
            if agent.budget.available < agent.budget.total * 0.2:
                self.warn_low_budget(agent_id)
            
            return True
        else:
            self.handle_budget_exhaustion(agent_id)
            return False
```

**Hook Integration**:
```python
async def budget_tracking_hook(input_data, tool_use_id, context) -> dict:
    """Pre-tool hook: Check and deduct budget"""
    agent_id = get_current_agent_id()
    tool_name = input_data.get('tool_name')
    
    tracker = BudgetTracker()
    if not tracker.track_tool_use(agent_id, tool_name):
        return {
            'decision': 'block',
            'systemMessage': 'BUDGET EXHAUSTED. Request more or complete task.'
        }
    
    return {}
```

**Dependencies**: Issue 1.3 (Shared Budget System base implementation)

**Estimated Effort**: 6-8 hours

**Files to Create**:
- `sixspec/agents/budget_tracker.py`
- `sixspec/mcp/hooks/budget_tracking_hook.py`
- `tests/agents/test_budget_tracker.py`

---

## PHASE 2: AGENT TYPES

### Issue 2.4: Implement Strategic Agent Template

**Epic**: Agent Templates

**Description**:
Create template and base class for Strategic Agents that execute top-down approaches based on organizational beliefs.

**Background**:
- Strategic agents implement APPROACH (L2-BEHAVIORS/strategic/)
- Execute plans derived from mission → identity → beliefs → capabilities
- Confidence: 0.60-0.85 (based on assumptions)
- Output: .w5h1 files documenting strategic initiatives

**Acceptance Criteria**:
- [ ] Create StrategicAgent base class
- [ ] Define standard system prompt template with placeholders:
  - {org_mission} from L6
  - {org_identity} from L5
  - {relevant_beliefs} from L4
  - {available_capabilities} from L3
- [ ] Implement agent initialization with org context
- [ ] Default tools: Read, Write, Grep, WebSearch
- [ ] Output validation: creates valid .w5h1 files in L2-BEHAVIORS/strategic/
- [ ] Purpose propagation check: agent mission traces to org
- [ ] Example implementation: MarketEntryAgent
- [ ] Unit tests for template instantiation

**Implementation Details**:
```python
class StrategicAgent:
    """
    Strategic Agent: Executes top-down approach
    Position: L2-BEHAVIORS/strategic/
    Confidence: 0.60-0.85 (assumption-based)
    """
    
    def __init__(self, org: DiltsOrganization, mission_from_org: str):
        self.agent_dilts = AgentDilts(
            agent_id=self.generate_id(),
            org_context=org.get_context(),
            spawn_level="L4-BELIEFS"  # Spawned by beliefs
        )
        
        # L6: Mission from org
        self.mission = mission_from_org
        
        # L5: Identity from template
        self.identity = self.create_identity()
        
        # L3: Capabilities from middle management
        self.capabilities = org.middle_management.provision_agent(
            mission=self.mission,
            agent_type="strategic"
        )
        
        # Budget
        self.budget = org.budget_manager.allocate_agent_budget(
            agent_type="strategic",
            estimated_complexity="medium"
        )
    
    def create_identity(self) -> Dict:
        """L5: Define strategic agent identity"""
        return {
            'role': 'Strategic Execution Agent',
            'who': 'Validator and executor of strategic approaches',
            'approach': 'Measured initiatives to serve market through identity',
            'values': ['alignment', 'validation', 'evidence']
        }
    
    def to_agent_definition(self) -> AgentDefinition:
        """Convert to Claude AgentDefinition"""
        return AgentDefinition(
            description=f"Strategic agent: {self.mission}",
            prompt=self.generate_system_prompt(),
            tools=self.capabilities['tools'],
            model="sonnet"
        )
    
    def generate_system_prompt(self) -> str:
        """Generate system prompt from agent Dilts"""
        return f"""
You are a Strategic Agent.

YOUR MISSION (L6): {self.mission}

YOUR IDENTITY (L5):
{yaml.dump(self.identity)}

YOUR CAPABILITIES (L3):
- Tools: {', '.join(self.capabilities['tools'])}
- Budget: {self.budget.available} tokens remaining

YOUR ROLE:
Execute top-down strategic initiatives based on organizational beliefs.
Document your approach in L2-BEHAVIORS/strategic/ as .w5h1 files.

CONFIDENCE: Your strategies are based on assumptions (0.60-0.85).
Always check belief confidence before executing high-risk actions.
"""
```

**Dependencies**: 
- Issue 2.1 (Agent Dilts Structure)
- Issue 1.1 (Permission Matrix)
- Issue 1.3 (Budget System)

**Estimated Effort**: 10-12 hours

**Files to Create**:
- `sixspec/agents/strategic_agent.py`
- `.agents/templates/strategic-agent-template.yaml`
- `examples/agents/market_entry_agent.py`
- `tests/agents/test_strategic_agent.py`

---

### Issue 2.5: Implement Tactical Agent Template

**Epic**: Agent Templates

**Description**:
Create template and base class for Tactical Agents that process bottom-up feedback and update organizational knowledge.

**Background**:
- Tactical agents implement RESPONSE (L2-BEHAVIORS/tactical/)
- Process observations from L1-ENVIRONMENT
- Confidence: 0.85-1.0 (observation-based, not assumption-based)
- Output: .w5h1 files documenting learnings and belief updates

**Acceptance Criteria**:
- [ ] Create TacticalAgent base class
- [ ] Define system prompt template emphasizing:
  - Observation over assumption
  - Evidence collection
  - Belief updating
  - High-confidence outputs
- [ ] Default tools: Read, Grep, Edit (primarily analysis, not creation)
- [ ] Output validation: creates .w5h1 files in L2-BEHAVIORS/tactical/
- [ ] Belief update suggestions: flags beliefs for validation/invalidation
- [ ] Example implementation: FeedbackAnalyzerAgent
- [ ] Unit tests for observation processing

**Implementation Details**:
```python
class TacticalAgent:
    """
    Tactical Agent: Processes market feedback
    Position: L2-BEHAVIORS/tactical/
    Confidence: 0.85-1.0 (observation-based)
    """
    
    def __init__(self, org: DiltsOrganization, observation_source: str):
        self.agent_dilts = AgentDilts(
            agent_id=self.generate_id(),
            org_context=org.get_context(),
            spawn_level="L1-ENVIRONMENT"  # Spawned by environment observations
        )
        
        # L6: Mission = Observe and learn
        self.mission = f"Analyze {observation_source} and update organizational understanding"
        
        # L5: Identity
        self.identity = {
            'role': 'Tactical Response Agent',
            'who': 'Observer and learner from market feedback',
            'approach': 'Evidence-based analysis with high confidence',
            'values': ['truth', 'empiricism', 'adaptation']
        }
        
        # L3: Capabilities (typically read-heavy)
        self.capabilities = org.middle_management.provision_agent(
            mission=self.mission,
            agent_type="tactical"
        )
    
    def to_agent_definition(self) -> AgentDefinition:
        return AgentDefinition(
            description=f"Tactical agent: {self.mission}",
            prompt=self.generate_system_prompt(),
            tools=self.capabilities['tools'],
            model="sonnet"
        )
    
    def generate_system_prompt(self) -> str:
        return f"""
You are a Tactical Response Agent.

YOUR MISSION (L6): {self.mission}

YOUR IDENTITY (L5):
{yaml.dump(self.identity)}

YOUR ROLE:
Process market feedback and update organizational understanding.

PROCESS:
1. OBSERVE: Analyze data from L1-ENVIRONMENT/
2. ANALYZE: Identify patterns with high confidence
3. UPDATE: Flag beliefs for validation/invalidation
4. REPORT: Document learnings in L2-BEHAVIORS/tactical/

CONFIDENCE: Base findings on evidence (0.85-1.0).
Always include sample sizes and data sources.
"""
```

**Dependencies**: Issue 2.1 (Agent Dilts Structure)

**Estimated Effort**: 8-10 hours

**Files to Create**:
- `sixspec/agents/tactical_agent.py`
- `.agents/templates/tactical-agent-template.yaml`
- `examples/agents/feedback_analyzer_agent.py`
- `tests/agents/test_tactical_agent.py`

---

### Issue 2.6: Implement Belief Validator Agent

**Epic**: Agent Templates

**Description**:
Create Belief Validator agent that systematically validates or invalidates organizational assumptions based on evidence from tactical agents.

**Background**:
- Validators move beliefs between assumptions/ → validated/ or invalidated/
- Update confidence scores based on evidence quality
- Critical for the learning loop to close
- Operates at L4-BELIEFS level

**Acceptance Criteria**:
- [ ] Create BeliefValidatorAgent class
- [ ] Implement belief identification logic (finds beliefs needing validation)
- [ ] Implement evidence analysis (supporting + contradicting)
- [ ] Confidence calculation based on evidence:
  - Sample size
  - Effect size
  - Statistical significance (if applicable)
- [ ] File movement: assumptions/ → validated/ or invalidated/
- [ ] Evidence trail documentation in moved files
- [ ] Alert mechanism: notify strategic agents of validated/invalidated beliefs
- [ ] Example: validate pricing assumption
- [ ] Integration test: full validation workflow

**Implementation Details**:
```python
class BeliefValidatorAgent:
    """
    Validates organizational assumptions based on evidence
    Position: L4-BELIEFS/
    Function: Move beliefs, update confidence
    """
    
    def validate_belief(self, belief_path: str, evidence: List[Dict]) -> ValidationResult:
        """Validate belief based on evidence"""
        
        current_belief = load_w5h1(belief_path)
        
        # Analyze evidence
        supporting = [e for e in evidence if e['type'] == 'supporting']
        contradicting = [e for e in evidence if e['type'] == 'contradicting']
        
        # Calculate confidence
        new_confidence = self.calculate_confidence(
            supporting=supporting,
            contradicting=contradicting,
            sample_sizes=[e['sample_size'] for e in evidence]
        )
        
        # Determine status
        if new_confidence > 0.85:
            status = "validated"
            move_to = "L4-BELIEFS/assumptions/validated/"
        elif new_confidence < 0.50:
            status = "invalidated"
            move_to = "L4-BELIEFS/assumptions/invalidated/"
        else:
            status = "needs_more_evidence"
            move_to = None
        
        return ValidationResult(
            original_confidence=current_belief.confidence,
            new_confidence=new_confidence,
            status=status,
            move_to=move_to,
            evidence_summary=self.summarize_evidence(evidence)
        )
```

**Dependencies**: 
- Issue 2.5 (Tactical Agent - provides evidence)
- Issue 2.1 (Agent Dilts)

**Estimated Effort**: 10-12 hours

**Files to Create**:
- `sixspec/agents/belief_validator.py`
- `sixspec/agents/evidence_analyzer.py`
- `.agents/templates/validator-agent-template.yaml`
- `tests/agents/test_belief_validator.py`

---

## PHASE 3: LEARNING LOOP

### Issue 3.1: Implement Strategy-Tactics Cycle Orchestrator

**Epic**: Multi-Agent Orchestration

**Description**:
Create orchestrator that coordinates the complete learning cycle: strategy execution → environment response → tactical analysis → belief validation → refined strategy.

**Background**:
- The learning loop is the core value proposition
- Requires coordinating multiple agent types
- Must handle async operations
- Should track cycle metrics (learning rate)

**Acceptance Criteria**:
- [ ] Create LearningCycleOrchestrator class
- [ ] Implement cycle phases:
  1. Strategic phase (spawn strategic agent)
  2. Execution phase (agent acts on environment)
  3. Observation phase (collect feedback)
  4. Tactical phase (spawn tactical agent to analyze)
  5. Validation phase (spawn validator to update beliefs)
  6. Refinement phase (next strategy with updated beliefs)
- [ ] Phase transition logic
- [ ] Error handling and recovery at each phase
- [ ] Cycle metrics: confidence deltas, beliefs updated, time per cycle
- [ ] Integration test: full cycle end-to-end
- [ ] Example: complete learning cycle for pricing validation

**Implementation Details**:
```python
class LearningCycleOrchestrator:
    """Orchestrates the complete strategic → tactical → validation cycle"""
    
    def __init__(self, org: DiltsOrganization):
        self.org = org
        self.registry = AgentRegistry()
        self.middle_management = MiddleManagement(org)
    
    async def run_cycle(self, initial_strategy: str) -> CycleResult:
        """Execute complete learning cycle"""
        
        metrics = CycleMetrics()
        
        # Phase 1: Strategic Approach
        strategic_agent = self.spawn_strategic_agent(initial_strategy)
        strategy_result = await strategic_agent.execute()
        metrics.strategy_confidence = strategy_result.confidence
        
        # Phase 2: Environment Response (simulated or real)
        env_feedback = await self.collect_environment_feedback()
        
        # Phase 3: Tactical Response
        tactical_agent = self.spawn_tactical_agent(env_feedback)
        tactical_result = await tactical_agent.analyze()
        metrics.observations_confidence = tactical_result.confidence
        
        # Phase 4: Belief Validation
        validator = self.spawn_validator_agent(tactical_result.belief_flags)
        validation_result = await validator.validate()
        metrics.beliefs_updated = validation_result.beliefs_updated
        metrics.confidence_delta = validation_result.average_confidence_change
        
        # Phase 5: Refined Strategy
        refined_beliefs = self.org.reload_beliefs()
        next_strategy = self.generate_next_strategy(
            previous_result=strategy_result,
            validated_beliefs=refined_beliefs
        )
        metrics.refined_confidence = calculate_strategy_confidence(next_strategy, refined_beliefs)
        
        return CycleResult(
            cycle_number=self.cycle_count,
            metrics=metrics,
            next_strategy=next_strategy
        )
    
    def spawn_strategic_agent(self, strategy: str) -> StrategicAgent:
        """Spawn strategic agent with org context"""
        pass
    
    def spawn_tactical_agent(self, feedback_data: Dict) -> TacticalAgent:
        """Spawn tactical agent to process feedback"""
        pass
    
    def spawn_validator_agent(self, beliefs_to_check: List[str]) -> BeliefValidatorAgent:
        """Spawn validator for specific beliefs"""
        pass
```

**Dependencies**: 
- Issue 2.4 (Strategic Agent)
- Issue 2.5 (Tactical Agent)
- Issue 2.6 (Validator Agent)

**Estimated Effort**: 12-15 hours

**Files to Create**:
- `sixspec/orchestration/learning_cycle.py`
- `sixspec/orchestration/metrics.py`
- `tests/orchestration/test_learning_cycle.py`
- `examples/orchestration/full_cycle_example.py`

---

### Issue 3.2: Implement Learning Rate Metrics

**Epic**: Organizational Intelligence Metrics

**Description**:
Create metrics system to measure how fast the organization learns (belief validation rate, confidence improvement, cycle efficiency).

**Background**:
- Need to measure if the learning loop is working
- Metrics prove value of the system
- Can optimize based on performance data

**Acceptance Criteria**:
- [ ] Define learning rate metrics:
  - Beliefs validated per cycle
  - Average confidence increase per cycle
  - Time from assumption → validated
  - Strategy success rate (based on tactical feedback)
  - Budget efficiency (value per token spent)
- [ ] Implement LearningRateTracker class
- [ ] Track across multiple cycles
- [ ] Generate reports and visualizations
- [ ] Identify bottlenecks (slow validation, low confidence gains)
- [ ] Dashboard or CLI command to view metrics
- [ ] Export to .w5h1 format for org knowledge

**Implementation Details**:
```python
@dataclass
class LearningMetrics:
    cycle_number: int
    beliefs_validated: int
    beliefs_invalidated: int
    average_confidence_before: float
    average_confidence_after: float
    confidence_delta: float
    cycle_duration_seconds: float
    budget_consumed: int
    strategy_success_score: float  # 0.0-1.0 based on tactical feedback

class LearningRateTracker:
    def track_cycle(self, cycle_result: CycleResult):
        """Record metrics for a complete cycle"""
        pass
    
    def calculate_learning_rate(self) -> float:
        """Calculate org learning rate: confidence gain per cycle"""
        recent_cycles = self.get_recent_cycles(n=10)
        total_delta = sum(c.confidence_delta for c in recent_cycles)
        return total_delta / len(recent_cycles)
    
    def generate_report(self) -> str:
        """Generate learning metrics report"""
        return f"""
        Learning Rate: {self.calculate_learning_rate():.3f} per cycle
        Beliefs Validated: {self.total_validated}
        Beliefs Invalidated: {self.total_invalidated}
        Avg Cycle Time: {self.avg_cycle_time}s
        Budget Efficiency: {self.value_per_token:.2f}
        """
```

**Dependencies**: Issue 3.1 (Learning Cycle Orchestrator)

**Estimated Effort**: 6-8 hours

**Files to Create**:
- `sixspec/metrics/learning_rate.py`
- `sixspec/cli/commands/metrics.py`
- `tests/metrics/test_learning_rate.py`

---

## PHASE 3: ADVANCED FEATURES

### Issue 3.3: Implement Dynamic Permission Updates

**Epic**: Middle Management Layer

**Description**:
Implement automatic permission expansion as beliefs get validated—agents working in domains with high-confidence beliefs get broader tool access.

**Background**:
- As org learns, agents should get more autonomy
- Validated beliefs → expand permissions
- Invalidated beliefs → restrict permissions or pivot
- Creates positive feedback loop: validation → capability → efficiency

**Acceptance Criteria**:
- [ ] Monitor belief validation events
- [ ] Trigger permission recalculation on validation/invalidation
- [ ] Identify agents affected by belief change
- [ ] Update agent capabilities in real-time (for active agents)
- [ ] Log permission changes with justification
- [ ] Notification to affected agents
- [ ] Rollback if belief later invalidated
- [ ] Integration test: validate belief → agent gains tools

**Implementation Details**:
```python
class DynamicPermissionManager:
    """Updates agent permissions based on belief validation"""
    
    def on_belief_validated(self, belief: W5H1, validation_result: ValidationResult):
        """Handle belief validation event"""
        
        old_confidence = belief.confidence
        new_confidence = validation_result.new_confidence
        
        if new_confidence > 0.85 and old_confidence < 0.85:
            # Belief crossed validation threshold
            affected_agents = self.find_agents_by_belief_domain(belief.domain)
            
            for agent in affected_agents:
                if agent.status == "active":
                    # Expand permissions
                    new_permissions = self.calculate_permissions(new_confidence)
                    self.update_agent_permissions(agent.agent_id, new_permissions)
                    
                    # Notify agent
                    self.notify_agent(
                        agent.agent_id,
                        f"Permissions expanded: {belief.name} validated (confidence: {new_confidence})"
                    )
```

**Dependencies**: 
- Issue 1.1 (Permission Matrix)
- Issue 2.6 (Belief Validator)

**Estimated Effort**: 8-10 hours

**Files to Create**:
- `sixspec/agents/dynamic_permissions.py`
- `tests/agents/test_dynamic_permissions.py`

---

### Issue 3.4: Implement Subagent Spawning with Budget Allocation

**Epic**: Multi-Agent Orchestration

**Description**:
Enable agents to spawn their own subagents (fractal recursion), with parent budget shared across all children.

**Background**:
- Agents may need specialized subagents for subtasks
- Subagents inherit mission context from parent
- Budget is shared: parent allocates slice to subagent
- Prevents infinite recursion via budget limits

**Acceptance Criteria**:
- [ ] Create MCP tool: `spawn_subagent`
- [ ] Subagent inherits parent's L6 mission context
- [ ] Subagent gets own L5 identity (defined in spawn request)
- [ ] Budget allocation: parent reserves budget for subagent
- [ ] Budget release: return unused budget when subagent completes
- [ ] Max depth limit (prevent infinite recursion)
- [ ] Parent-child relationship tracking
- [ ] Subagent completion handling (success/failure)
- [ ] Integration test: agent spawns subagent, both share budget

**Implementation Details**:
```python
@tool("spawn_subagent",
      "Spawn a specialized subagent for a specific subtask",
      {
          "subagent_type": str,  # "research", "analysis", "validation"
          "mission": str,         # What the subagent should accomplish
          "budget_allocation": int,  # Tokens to allocate
          "required_tools": list  # Tools subagent needs
      })
async def spawn_subagent(args: dict) -> dict:
    parent = get_current_agent()
    
    # Check budget availability
    if args['budget_allocation'] > parent.budget.available:
        return {
            "is_error": True,
            "content": [{
                "type": "text",
                "text": f"Insufficient budget. Available: {parent.budget.available}, Requested: {args['budget_allocation']}"
            }]
        }
    
    # Allocate budget
    parent.budget.allocate_to_subagent(args['budget_allocation'])
    
    # Create subagent
    subagent = create_subagent(
        parent_id=parent.agent_id,
        subagent_type=args['subagent_type'],
        mission=args['mission'],  # Subagent's L6
        budget=args['budget_allocation'],
        tools=args['required_tools'],
        max_depth=parent.depth + 1
    )
    
    # Register
    registry.register_agent(subagent)
    
    return {
        "content": [{
            "type": "text",
            "text": f"Subagent spawned: {subagent.agent_id} | Budget: {args['budget_allocation']} tokens"
        }]
    }

def create_subagent(parent_id, subagent_type, mission, budget, tools, max_depth):
    """Create subagent instance with inheritance"""
    
    parent = registry.get_agent(parent_id)
    
    # Prevent infinite recursion
    if max_depth > 3:
        raise MaxDepthExceededError("Subagent depth limit reached")
    
    subagent = AgentInstance(
        agent_id=generate_id(),
        agent_type=subagent_type,
        spawn_level=parent.spawn_level,  # Inherit spawn context
        parent_agent_id=parent_id,
        status="active",
        budget=AgentBudget(total=budget, used=0, reserved=0),
        dilts=AgentDilts(
            agent_id=generate_id(),
            org_context={
                'parent_mission': parent.mission,
                'inherited_mission': mission
            },
            spawn_level=parent.spawn_level
        ),
        depth=max_depth
    )
    
    return subagent
```

**Dependencies**: 
- Issue 1.3 (Shared Budget System)
- Issue 2.1 (Agent Dilts)
- Issue 2.2 (Agent Registry)

**Estimated Effort**: 10-12 hours

**Files to Create**:
- `sixspec/mcp/tools/spawn_subagent.py`
- `sixspec/agents/subagent_manager.py`
- `tests/agents/test_subagent_spawning.py`

---

### Issue 3.5: Implement Cross-Agent Belief Sharing

**Epic**: Organizational Intelligence

**Description**:
Enable agents to share validated beliefs at their own L4 level, creating a distributed learning network where insights propagate across agents.

**Background**:
- Multiple agents may work on related tasks
- Validated learnings should be shared
- Prevents redundant validation
- Creates "collective intelligence"

**Acceptance Criteria**:
- [ ] Create shared belief store at `.agents/shared-beliefs/`
- [ ] Agents can publish validated beliefs to shared store
- [ ] Agents can query shared store before making assumptions
- [ ] Belief attribution (which agent validated it)
- [ ] Confidence aggregation (multiple agents confirm same belief)
- [ ] MCP tool: `query_shared_beliefs`
- [ ] MCP tool: `publish_belief`
- [ ] Conflict detection (agents with contradicting beliefs)
- [ ] Integration test: two agents share and consume beliefs

**Implementation Details**:
```python
class SharedBeliefStore:
    """Distributed belief store for agent-level learning"""
    
    def publish_belief(self, agent_id: str, belief: Dict):
        """Agent publishes validated belief"""
        belief_entry = {
            'belief': belief,
            'validated_by': agent_id,
            'confidence': belief['confidence'],
            'evidence': belief['evidence'],
            'timestamp': datetime.now()
        }
        self.store.add(belief_entry)
        self.notify_interested_agents(belief)
    
    def query_beliefs(self, domain: str, min_confidence: float = 0.70) -> List[Dict]:
        """Query beliefs in a domain with min confidence"""
        return [
            b for b in self.store 
            if b['belief']['domain'] == domain 
            and b['confidence'] >= min_confidence
        ]
    
    def aggregate_confidence(self, belief_key: str) -> float:
        """Aggregate confidence from multiple agents validating same belief"""
        beliefs = [b for b in self.store if b['belief']['key'] == belief_key]
        if not beliefs:
            return 0.0
        
        # Weighted average by evidence quality
        total_weight = sum(b['evidence']['sample_size'] for b in beliefs)
        weighted_conf = sum(
            b['confidence'] * b['evidence']['sample_size'] 
            for b in beliefs
        )
        return weighted_conf / total_weight if total_weight > 0 else 0.0
```

**MCP Tools**:
```python
@tool("query_shared_beliefs", 
      "Query beliefs validated by other agents",
      {"domain": str, "min_confidence": float})
async def query_shared_beliefs(args: dict) -> dict:
    store = SharedBeliefStore()
    beliefs = store.query_beliefs(args['domain'], args.get('min_confidence', 0.70))
    return {"content": [{"type": "text", "text": yaml.dump(beliefs)}]}

@tool("publish_belief",
      "Share a validated belief with other agents",
      {"belief": dict, "evidence": dict})
async def publish_belief(args: dict) -> dict:
    agent_id = get_current_agent_id()
    store = SharedBeliefStore()
    store.publish_belief(agent_id, args['belief'])
    return {"content": [{"type": "text", "text": "Belief published to shared store"}]}
```

**Dependencies**: Issue 2.6 (Belief Validator)

**Estimated Effort**: 8-10 hours

**Files to Create**:
- `sixspec/agents/shared_beliefs.py`
- `sixspec/mcp/tools/shared_belief_tools.py`
- `.agents/shared-beliefs/store.json`
- `tests/agents/test_shared_beliefs.py`

---

## PHASE 4: INTEGRATION & POLISH

### Issue 4.1: Create CLI Commands for Agent Management

**Epic**: Developer Experience

**Description**:
Create CLI commands for managing agents: list active, inspect, provision, kill, view budgets, etc.

**Acceptance Criteria**:
- [ ] `sixspec agent list` - List all active agents
- [ ] `sixspec agent inspect <agent-id>` - View agent details (Dilts, budget, logs)
- [ ] `sixspec agent provision <type>` - Manually provision agent
- [ ] `sixspec agent kill <agent-id>` - Terminate agent
- [ ] `sixspec agent budget <agent-id>` - View budget status
- [ ] `sixspec agent logs <agent-id>` - View agent action logs
- [ ] `sixspec agent tree` - View agent hierarchy (parent-child)
- [ ] Output formatting (table, JSON, YAML)
- [ ] Help documentation for each command

**Dependencies**: Issue 2.2 (Agent Registry)

**Estimated Effort**: 6-8 hours

**Files to Create**:
- `sixspec/cli/agent_commands.py`
- `tests/cli/test_agent_commands.py`

---

### Issue 4.2: Create Agent Dashboard Visualization

**Epic**: Developer Experience

**Description**:
Create web-based dashboard to visualize active agents, learning cycles, belief validation, and budget consumption.

**Acceptance Criteria**:
- [ ] Web dashboard (HTML/CSS/JS)
- [ ] Real-time agent status display
- [ ] Learning cycle visualization (flow diagram)
- [ ] Belief confidence trends over time
- [ ] Budget consumption charts
- [ ] Agent hierarchy tree view
- [ ] Refresh/polling for live updates
- [ ] Export reports (PDF/PNG)

**Implementation Details**:
- Static HTML served locally
- JavaScript fetch from agent registry JSON
- D3.js or similar for visualizations
- Auto-refresh every 5 seconds

**Dependencies**: 
- Issue 2.2 (Agent Registry)
- Issue 3.2 (Learning Metrics)

**Estimated Effort**: 10-12 hours

**Files to Create**:
- `public/agent-dashboard.html`
- `public/js/agent-dashboard.js`
- `public/css/agent-dashboard.css`

---

### Issue 4.3: Implement Agent Action Audit Trail

**Epic**: Compliance & Governance

**Description**:
Create comprehensive audit trail for all agent actions: tool usage, budget consumption, belief updates, and decision reasoning.

**Background**:
- Compliance requires full traceability
- Debug agent behavior by reviewing logs
- Learn from agent successes/failures
- Enable replay/analysis of cycles

**Acceptance Criteria**:
- [ ] Log every tool execution with:
  - Agent ID
  - Tool name and inputs
  - Timestamp
  - Budget consumed
  - Result/error
- [ ] Log every belief update with:
  - Agent ID
  - Belief updated
  - Confidence change
  - Evidence used
- [ ] Log every budget event (allocation, consumption, request)
- [ ] Structured log format (JSON Lines)
- [ ] Query interface: filter by agent, time, action type
- [ ] Export audit trail to .w5h1 format
- [ ] Retention policy (archive old logs)

**Implementation Details**:
```python
class AuditTrail:
    def log_tool_use(self, event: ToolUseEvent):
        """Log tool execution"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'tool_use',
            'agent_id': event.agent_id,
            'tool_name': event.tool_name,
            'input': event.input_data,
            'output': event.result,
            'budget_consumed': event.budget_cost,
            'success': event.success
        }
        self.append_log(entry)
    
    def query_logs(self, filters: Dict) -> List[Dict]:
        """Query audit trail with filters"""
        pass
    
    def export_to_w5h1(self, agent_id: str, output_path: str):
        """Export agent's action log as .w5h1 file"""
        pass
```

**Dependencies**: Issue 2.2 (Agent Registry)

**Estimated Effort**: 6-8 hours

**Files to Create**:
- `sixspec/agents/audit_trail.py`
- `.agents/logs/audit.jsonl`
- `tests/agents/test_audit_trail.py`

---

## PHASE 4: REAL-WORLD TESTING

### Issue 4.4: End-to-End Integration Test

**Epic**: Quality Assurance

**Description**:
Create comprehensive end-to-end test that validates the entire system: agent provisioning → strategy execution → tactical feedback → belief validation → refined strategy.

**Background**:
- Need confidence that all pieces work together
- Test realistic scenario with actual Claude API
- Validate learning loop improves confidence
- Catch integration bugs before production

**Acceptance Criteria**:
- [ ] Test scenario: Validate pricing assumption
  1. Create org with pricing belief (confidence 0.65)
  2. Provision strategic agent
  3. Agent executes pricing strategy
  4. Simulate market feedback (or use real A/B test data)
  5. Tactical agent analyzes feedback
  6. Validator updates belief confidence
  7. Verify belief moved to validated/invalidated
  8. Verify next strategy uses updated belief
- [ ] Assert at each phase:
  - Correct .w5h1 files created
  - Purpose propagation maintained
  - Budget tracking accurate
  - Confidence changes as expected
- [ ] Test with actual Claude Agent SDK (not mocked)
- [ ] Measure learning rate (confidence delta)
- [ ] Generate test report with metrics

**Dependencies**: All previous issues (final integration)

**Estimated Effort**: 12-15 hours

**Files to Create**:
- `tests/integration/test_full_learning_cycle.py`
- `tests/integration/fixtures/pricing_scenario.yaml`
- `tests/integration/README.md`

---

### Issue 4.5: Create Example: Real Organization Setup

**Epic**: Documentation & Examples

**Description**:
Create complete real-world example organization with agents configured and ready to run, demonstrating the full system in action.

**Background**:
- Need working example for users to clone and customize
- Showcase all features: provisioning, learning loop, belief validation
- Documentation by demonstration

**Acceptance Criteria**:
- [ ] Create example organization: "TechStartup-AI-Tools"
- [ ] Complete Dilts structure (L6-L1) with realistic content
- [ ] 3-5 beliefs in L4-BELIEFS/assumptions/ needing validation
- [ ] Configured agents:
  - Strategic: Market entry agent
  - Tactical: Feedback analyzer
  - Validator: Belief validator
- [ ] Agent configuration files
- [ ] Sample data in L1-ENVIRONMENT/ for tactical analysis
- [ ] Run script that executes full learning cycle
- [ ] README with step-by-step walkthrough
- [ ] Expected outputs documented

**Files to Create**:
- `examples/real-org-setup/` directory with complete structure
- `examples/real-org-setup/run_learning_cycle.py`
- `examples/real-org-setup/README.md`
- `examples/real-org-setup/TechStartup-AI-Tools/` (full org)

**Dependencies**: All Phase 1-3 issues

**Estimated Effort**: 8-10 hours

---

## PHASE 5: OPTIMIZATION & SCALING

### Issue 5.1: Implement Agent Dilts Query Caching

**Epic**: Performance Optimization

**Description**:
Add caching layer for lazy-loaded agent Dilts queries to prevent redundant lookups and improve performance.

**Background**:
- Agents may query same Dilts level multiple times
- Each query hits filesystem/org structure
- Caching with TTL improves performance
- Cache invalidation on org changes

**Acceptance Criteria**:
- [ ] Implement LRU cache for Dilts queries
- [ ] TTL (time-to-live): 300 seconds (5 minutes)
- [ ] Cache invalidation triggers:
  - Org belief updated
  - Agent permissions changed
  - Manual cache clear
- [ ] Cache hit/miss metrics
- [ ] Memory limits for cache size
- [ ] Unit tests for cache behavior (hits, misses, invalidation)

**Implementation Details**:
```python
from functools import lru_cache
from datetime import datetime, timedelta

class DiltsQueryCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self.cache = {}
        self.timestamps = {}
    
    def get(self, agent_id: str, level: str) -> Optional[Dict]:
        """Get cached Dilts level if not stale"""
        key = f"{agent_id}:{level}"
        if key in self.cache:
            if datetime.now() - self.timestamps[key] < timedelta(seconds=self.ttl):
                return self.cache[key]  # Cache hit
            else:
                del self.cache[key]  # Expired
        return None  # Cache miss
    
    def set(self, agent_id: str, level: str, data: Dict):
        """Cache Dilts level data"""
        key = f"{agent_id}:{level}"
        self.cache[key] = data
        self.timestamps[key] = datetime.now()
    
    def invalidate(self, agent_id: str, level: Optional[str] = None):
        """Invalidate cache for agent (all or specific level)"""
        if level:
            key = f"{agent_id}:{level}"
            if key in self.cache:
                del self.cache[key]
        else:
            # Invalidate all levels for this agent
            keys_to_delete = [k for k in self.cache if k.startswith(f"{agent_id}:")]
            for key in keys_to_delete:
                del self.cache[key]
```

**Dependencies**: Issue 2.1 (Agent Dilts - lazy loading)

**Estimated Effort**: 4-6 hours

**Files to Create**:
- `sixspec/agents/dilts_cache.py`
- `tests/agents/test_dilts_cache.py`

---

### Issue 5.2: Implement Budget Request Auto-Approval Logic

**Epic**: Middle Management Layer

**Description**:
Enhance middle management with intelligent auto-approval for budget increase requests based on agent performance and mission criticality.

**Background**:
- Manual approval for every budget request doesn't scale
- High-performing agents should get auto-approval
- Critical missions warrant larger budgets
- Need heuristics for auto-approval

**Acceptance Criteria**:
- [ ] Track agent performance metrics:
  - Beliefs validated by this agent
  - Strategy success rate
  - Budget efficiency (value per token)
- [ ] Auto-approval heuristics:
  - Agent has validated 3+ beliefs → auto-approve
  - Mission criticality high → auto-approve
  - Requested amount < 20% of total → auto-approve
  - Otherwise → escalate to human
- [ ] Budget cap per agent type
- [ ] Historical request analysis (learn approval patterns)
- [ ] Notification system for auto-approvals
- [ ] Override mechanism (human can always approve/deny)

**Implementation Details**:
```python
class BudgetApprovalEngine:
    def evaluate_budget_request(self, request: BudgetRequest) -> ApprovalDecision:
        """Intelligent budget request evaluation"""
        
        agent = registry.get_agent(request.agent_id)
        
        # Check agent performance
        performance = self.calculate_agent_performance(agent)
        
        # Check mission criticality
        criticality = self.assess_mission_criticality(agent.mission)
        
        # Check request size
        request_ratio = request.amount / agent.budget.total
        
        # Auto-approval criteria
        if performance.beliefs_validated >= 3:
            return ApprovalDecision(approved=True, reason="proven_performer")
        elif criticality == "high" and request_ratio < 0.5:
            return ApprovalDecision(approved=True, reason="critical_mission")
        elif request_ratio < 0.2:
            return ApprovalDecision(approved=True, reason="small_request")
        else:
            return ApprovalDecision(escalate=True, reason="needs_human_review")
```

**Dependencies**: 
- Issue 1.2 (Tool Request Workflow)
- Issue 2.3 (Budget Tracking)

**Estimated Effort**: 6-8 hours

**Files to Create**:
- `sixspec/agents/budget_approval.py`
- `tests/agents/test_budget_approval.py`

---

## PHASE 6: DOCUMENTATION & EXAMPLES

### Issue 6.1: Complete Agent Integration Tutorial

**Epic**: Documentation

**Description**:
Create comprehensive tutorial walking through agent setup, learning cycle, and organizational learning from first principles.

**Acceptance Criteria**:
- [ ] Step-by-step tutorial from scratch
- [ ] Create example organization
- [ ] Configure agents (strategic, tactical, validator)
- [ ] Run learning cycle
- [ ] Interpret results
- [ ] Troubleshooting section
- [ ] Best practices guide
- [ ] Code snippets for common patterns

**Estimated Effort**: 6-8 hours

**Files to Create**:
- `AGENT_TUTORIAL.md`
- `examples/agent-tutorial/` directory with working example

---

### Issue 6.2: Update Main Documentation

**Epic**: Documentation

**Description**:
Update existing SixSpec documentation to incorporate agent integration concepts.

**Acceptance Criteria**:
- [ ] Update ARCHITECTURE.md with agent layer
- [ ] Update README.md with agent features
- [ ] Update QUICKSTART.md with agent example
- [ ] Add agents section to API_REFERENCE.md
- [ ] Update DILTS_COMPLETE_PACKAGE.md with agent integration

**Dependencies**: All implementation complete

**Estimated Effort**: 4-6 hours

---

## SUMMARY OF OUTLINES

### Total Issues: 13

**Phase 1 - Foundation** (3 issues):
1. Permission Matrix (3-5h)
2. Tool Request Workflow (5-8h)
3. Shared Budget System (6-8h)

**Phase 2 - Agent Structure** (3 issues):
4. Agent Dilts Structure - Lazy Loaded (10-12h)
5. Agent Instance Management (8-10h)
6. Budget Tracking & Consumption (6-8h)

**Phase 3 - Agent Types** (3 issues):
7. Strategic Agent Template (10-12h)
8. Tactical Agent Template (8-10h)
9. Belief Validator Agent (10-12h)

**Phase 4 - Learning Loop** (3 issues):
10. Learning Cycle Orchestrator (12-15h)
11. Learning Rate Metrics (6-8h)
12. Dynamic Permission Updates (8-10h)

**Phase 5 - Advanced** (2 issues):
13. Subagent Spawning (10-12h)
14. Cross-Agent Belief Sharing (8-10h)

**Phase 6 - Optimization** (2 issues):
15. Dilts Query Caching (4-6h)
16. Budget Auto-Approval (6-8h)

**Phase 7 - Integration** (2 issues):
17. End-to-End Test (12-15h)
18. Real Organization Example (8-10h)

**Phase 8 - Documentation** (2 issues):
19. Agent Tutorial (6-8h)
20. Update Main Docs (4-6h)

### Total Estimated Effort: 150-190 hours

### Critical Path:
1. Permission Matrix (1.1)
2. Agent Dilts Structure (2.1)
3. Agent Registry (2.2)
4. Strategic Agent (2.4)
5. Tactical Agent (2.5)
6. Validator Agent (2.6)
7. Learning Cycle (3.1)
8. End-to-End Test (4.4)

---

## Notes for Linear Issue Creation

### Labels to Use:
- `epic:middle-management` - Issues 1.1, 1.2, 1.3, 3.3, 5.2
- `epic:agent-structure` - Issues 2.1, 2.2, 2.3
- `epic:agent-templates` - Issues 2.4, 2.5, 2.6
- `epic:orchestration` - Issues 3.1, 3.4
- `epic:metrics` - Issues 3.2, 3.5
- `epic:developer-experience` - Issues 4.1, 4.2
- `epic:compliance` - Issue 4.3
- `epic:optimization` - Issues 5.1, 5.2
- `epic:documentation` - Issues 6.1, 6.2

### Priority Levels:
- P0 (Critical): 1.1, 2.1, 2.2, 2.4, 2.5, 2.6, 3.1
- P1 (High): 1.2, 1.3, 2.3, 3.2, 4.4
- P2 (Medium): 3.3, 3.4, 4.1, 6.1, 6.2
- P3 (Low): 3.5, 4.2, 4.3, 5.1, 5.2, 4.5

### Dependencies Matrix:
See individual issues for specific dependencies listed.

---

## Ready for Review

These outlines provide:
- ✅ Clear scope per issue
- ✅ Specific acceptance criteria
- ✅ Code structure examples
- ✅ Effort estimates
- ✅ Dependencies mapped
- ✅ Files to create listed

**Next Step**: Review and approve outlines, then convert to Linear issues with proper formatting, labels, and relationships.
