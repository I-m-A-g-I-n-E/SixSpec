"""
Example: Agent Integration with Dilts Organizational Structure

This demonstrates how to use Claude's Agent SDK to create:
1. Strategic agents that execute top-down approaches
2. Tactical agents that process bottom-up feedback
3. Belief validators that update organizational knowledge
4. Orchestrators that coordinate the learning cycle
"""

import asyncio
from pathlib import Path
from typing import Dict, List
import yaml

# Note: Requires: pip install claude-agent-sdk
try:
    from claude_agent_sdk import (
        ClaudeSDKClient,
        ClaudeAgentOptions,
        AgentDefinition,
        AssistantMessage,
        TextBlock,
        HookMatcher,
        HookContext
    )
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    print("Warning: claude-agent-sdk not installed. Install with:")
    print("  pip install claude-agent-sdk")


class DiltsOrganization:
    """
    Represents an organization with Dilts structure and integrated agents.
    """
    
    def __init__(self, org_path: Path):
        self.org_path = Path(org_path)
        self.mission = self.load_spec("L6-MISSION/mission-statement.w5h1")
        self.identity = self.load_spec("L5-IDENTITY/brand/brand-identity.w5h1")
    
    def load_spec(self, rel_path: str) -> Dict:
        """Load a W5H1 specification file"""
        file_path = self.org_path / rel_path
        if file_path.exists():
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def get_mission_statement(self) -> str:
        """Get the mission WHAT dimension"""
        if 'dimensions' in self.mission and 'WHAT' in self.mission['dimensions']:
            return self.mission['dimensions']['WHAT']['value']
        return "Mission not defined"
    
    def get_identity_statement(self) -> str:
        """Get the identity WHO dimension"""
        if 'dimensions' in self.identity and 'WHO' in self.identity['dimensions']:
            return self.identity['dimensions']['WHO']['value']
        return "Identity not defined"


class StrategicAgent:
    """
    Strategic Agent: Executes top-down approaches based on organizational beliefs
    
    Position: L2-BEHAVIORS/strategic/
    Function: Implement strategies to serve the market through identity
    Confidence: 0.60-0.85 (based on assumptions)
    """
    
    def __init__(self, org: DiltsOrganization):
        self.org = org
        self.agent_def = self.create_agent_definition()
    
    def create_agent_definition(self) -> 'AgentDefinition':
        """Create Claude agent definition for strategic execution"""
        
        mission = self.org.get_mission_statement()
        identity = self.org.get_identity_statement()
        
        prompt = f"""
You are the Strategic Agent for this organization.

ORGANIZATIONAL CONTEXT:
- Mission (L6): {mission}
- Identity (L5): {identity}

YOUR ROLE:
Execute top-down strategic initiatives to serve the market.

APPROACH:
1. Understand the strategic goal
2. Leverage organizational capabilities (L3)
3. Follow guiding beliefs (L4)
4. Act upon the environment (L1)
5. Document your approach in L2-BEHAVIORS/strategic/

CONFIDENCE:
Your strategies are based on beliefs (confidence: 0.60-0.85).
Flag when operating on low-confidence assumptions.

TOOLS:
- Read: Research market, read specifications
- Write: Document strategies, create plans
- WebSearch: Gather market intelligence
- Grep: Analyze existing organizational knowledge

OUTPUT:
Create .w5h1 files in L2-BEHAVIORS/strategic/ documenting:
- WHY: Purpose (from parent spec)
- WHAT: The strategic initiative
- HOW: The approach
- Confidence: Your confidence in this strategy
"""
        
        return AgentDefinition(
            description="Execute organizational strategy based on mission and beliefs",
            prompt=prompt,
            tools=["Read", "Write", "Grep", "WebSearch"],
            model="sonnet"
        )


class TacticalAgent:
    """
    Tactical Agent: Processes market feedback and updates organizational knowledge
    
    Position: L2-BEHAVIORS/tactical/
    Function: Observe environment responses and inform strategic refinement
    Confidence: 0.85-1.0 (based on observations)
    """
    
    def __init__(self, org: DiltsOrganization):
        self.org = org
        self.agent_def = self.create_agent_definition()
    
    def create_agent_definition(self) -> 'AgentDefinition':
        """Create Claude agent definition for tactical analysis"""
        
        prompt = f"""
You are the Tactical Agent for this organization.

YOUR ROLE:
Process market feedback and update organizational understanding.

PROCESS:
1. OBSERVE: Read data from L1-ENVIRONMENT/
   - Customer feedback
   - Market metrics
   - Competitive intelligence
   - Performance data

2. ANALYZE: Identify patterns and insights
   - What worked vs. what didn't?
   - Which assumptions are validated/invalidated?
   - What new capabilities are needed?

3. UPDATE: Revise organizational knowledge
   - Document learnings in L2-BEHAVIORS/tactical/
   - Flag beliefs for validation in L4-BELIEFS/
   - Suggest capability updates for L3-CAPABILITIES/

4. REPORT: Generate insights
   - Confidence in observations: 0.85-1.0 (direct evidence)
   - Evidence trail with sample sizes
   - Recommendations for strategic refinement

CONFIDENCE:
Your observations are based on real data (confidence: 0.85-1.0).
Always include evidence sources and sample sizes.

TOOLS:
- Read: Analyze feedback and metrics
- Write: Document learnings
- Grep: Find patterns in data
- Edit: Update existing specs

OUTPUT:
Create .w5h1 files in L2-BEHAVIORS/tactical/ documenting:
- WHERE: Data sources (L1)
- WHAT: Observations and learnings
- HOW: Analysis methodology
- Confidence: Based on evidence quality
- Impact: Which beliefs/capabilities need updating
"""
        
        return AgentDefinition(
            description="Analyze market feedback and update organizational beliefs",
            prompt=prompt,
            tools=["Read", "Write", "Edit", "Grep"],
            model="sonnet"
        )


class BeliefValidatorAgent:
    """
    Belief Validator: Validates or invalidates organizational assumptions
    
    Position: L4-BELIEFS/
    Function: Move assumptions to validated/ or invalidated/ based on evidence
    """
    
    def __init__(self, org: DiltsOrganization):
        self.org = org
        self.agent_def = self.create_agent_definition()
    
    def create_agent_definition(self) -> 'AgentDefinition':
        """Create Claude agent definition for belief validation"""
        
        prompt = """
You are the Belief Validator Agent.

YOUR ROLE:
Systematically validate or invalidate organizational assumptions.

PROCESS:
1. IDENTIFY beliefs needing validation:
   - Confidence < 0.70
   - Status: "validation_needed"
   - No recent validation

2. REVIEW evidence from tactical agents:
   - Read tactical reports from L2-BEHAVIORS/tactical/
   - Analyze supporting and contradicting evidence
   - Calculate confidence based on evidence quality

3. UPDATE beliefs:
   - If validated: Move to L4-BELIEFS/assumptions/validated/
   - If invalidated: Move to L4-BELIEFS/assumptions/invalidated/
   - Update confidence scores
   - Document evidence trail

4. ALERT strategic agents:
   - Validated beliefs enable higher-confidence strategies
   - Invalidated beliefs require strategic pivots

CONFIDENCE CALCULATION:
- Strong evidence (n>50): confidence 0.85-0.95
- Moderate evidence (n=20-50): confidence 0.70-0.84
- Weak evidence (n<20): confidence 0.50-0.69
- Insufficient evidence: keep in assumptions/, flag for more testing

OUTPUT:
- Updated .w5h1 files with new confidence scores
- Movement between directories (assumptions/ → validated/invalidated/)
- Validation reports with evidence summary
"""
        
        return AgentDefinition(
            description="Validate organizational assumptions based on evidence",
            prompt=prompt,
            tools=["Read", "Write", "Edit", "Grep"],
            model="sonnet"
        )


async def belief_confidence_hook(
    input_data: dict,
    tool_use_id: str | None,
    context: 'HookContext'
) -> dict:
    """
    Hook: Check belief confidence before strategic execution.
    Warn if strategy is based on low-confidence assumptions.
    """
    tool_name = input_data.get('tool_name', '')
    
    # If writing strategic files
    if tool_name == "Write" and "strategic" in str(input_data.get('file_path', '')):
        # In production, load and check related beliefs
        # For now, just log
        print("[HOOK] Checking belief confidence before strategic action...")
        
        return {
            'systemMessage': """
            REMINDER: Verify confidence of underlying beliefs before executing strategy.
            Low-confidence beliefs (< 0.70) should be validated first.
            """
        }
    
    return {}


async def learning_capture_hook(
    input_data: dict,
    tool_use_id: str | None,
    context: 'HookContext'
) -> dict:
    """
    Hook: Capture learnings after tactical analysis.
    Auto-document insights for future reference.
    """
    tool_name = input_data.get('tool_name', '')
    
    # If writing tactical files
    if tool_name == "Write" and "tactical" in str(input_data.get('file_path', '')):
        print("[HOOK] Capturing tactical learnings for organizational memory...")
        
        return {
            'systemMessage': """
            Tactical insight captured. Consider:
            1. Which beliefs should be updated?
            2. What new capabilities are needed?
            3. Should identity be refined?
            """
        }
    
    return {}


async def simple_strategic_example(org_path: Path):
    """
    Simple example: Strategic agent executes market research
    """
    if not AGENTS_AVAILABLE:
        print("Skipping agent example (claude-agent-sdk not installed)")
        return
    
    print("=" * 60)
    print("EXAMPLE 1: Strategic Agent - Market Research")
    print("=" * 60)
    
    org = DiltsOrganization(org_path)
    strategic = StrategicAgent(org)
    
    options = ClaudeAgentOptions(
        agents={"strategy": strategic.agent_def},
        allowed_tools=["Read", "Write", "Grep", "WebSearch"],
        permission_mode="acceptEdits",
        cwd=str(org_path)
    )
    
    async with ClaudeSDKClient(options=options) as client:
        await client.query("""
        @strategy: Research our top 3 competitors
        
        1. Use WebSearch to find competitor information
        2. Document findings in L2-BEHAVIORS/strategic/competitor-analysis.w5h1
        3. Follow W5H1 format with confidence scores
        4. Identify their key capabilities and positioning
        """)
        
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Strategic Agent: {block.text[:200]}...")


async def tactical_feedback_example(org_path: Path):
    """
    Example: Tactical agent analyzes customer feedback
    """
    if not AGENTS_AVAILABLE:
        print("Skipping agent example (claude-agent-sdk not installed)")
        return
    
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Tactical Agent - Feedback Analysis")
    print("=" * 60)
    
    org = DiltsOrganization(org_path)
    tactical = TacticalAgent(org)
    
    options = ClaudeAgentOptions(
        agents={"tactics": tactical.agent_def},
        allowed_tools=["Read", "Write", "Grep", "Edit"],
        permission_mode="acceptEdits",
        cwd=str(org_path),
        hooks={
            'PostToolUse': [
                HookMatcher(hooks=[learning_capture_hook])
            ]
        }
    )
    
    async with ClaudeSDKClient(options=options) as client:
        await client.query("""
        @tactics: Analyze customer feedback from Q1
        
        1. Read feedback files from L1-ENVIRONMENT/market/ (if they exist)
        2. Create simulated analysis if no files exist
        3. Document patterns and insights
        4. Output to L2-BEHAVIORS/tactical/q1-feedback-analysis.w5h1
        5. Flag which beliefs should be reviewed based on findings
        """)
        
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Tactical Agent: {block.text[:200]}...")


async def belief_validation_example(org_path: Path):
    """
    Example: Validator agent validates assumptions
    """
    if not AGENTS_AVAILABLE:
        print("Skipping agent example (claude-agent-sdk not installed)")
        return
    
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Belief Validator - Validate Assumptions")
    print("=" * 60)
    
    org = DiltsOrganization(org_path)
    validator = BeliefValidatorAgent(org)
    
    options = ClaudeAgentOptions(
        agents={"validator": validator.agent_def},
        allowed_tools=["Read", "Write", "Edit", "Grep"],
        permission_mode="acceptEdits",
        cwd=str(org_path)
    )
    
    async with ClaudeSDKClient(options=options) as client:
        await client.query("""
        @validator: Review beliefs needing validation
        
        1. List all files in L4-BELIEFS/assumptions/
        2. For each belief:
           - Check confidence score
           - Check validation status
           - Check evidence quality
        3. Recommend which beliefs to validate first
        4. Create validation plan for top 3 priorities
        """)
        
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Validator Agent: {block.text[:200]}...")


async def full_learning_cycle_example(org_path: Path):
    """
    Example: Complete learning cycle with multiple agents
    """
    if not AGENTS_AVAILABLE:
        print("Skipping agent example (claude-agent-sdk not installed)")
        return
    
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Full Learning Cycle")
    print("=" * 60)
    
    org = DiltsOrganization(org_path)
    
    # Create all agents
    strategic = StrategicAgent(org)
    tactical = TacticalAgent(org)
    validator = BeliefValidatorAgent(org)
    
    options = ClaudeAgentOptions(
        agents={
            "strategy": strategic.agent_def,
            "tactics": tactical.agent_def,
            "validator": validator.agent_def
        },
        allowed_tools=["Read", "Write", "Edit", "Grep", "WebSearch"],
        permission_mode="acceptEdits",
        cwd=str(org_path),
        hooks={
            'PreToolUse': [
                HookMatcher(matcher='Write', hooks=[belief_confidence_hook])
            ],
            'PostToolUse': [
                HookMatcher(hooks=[learning_capture_hook])
            ]
        }
    )
    
    async with ClaudeSDKClient(options=options) as client:
        # Phase 1: Strategic Approach
        print("\n--- PHASE 1: Strategic Approach ---")
        await client.query("""
        @strategy: Execute market entry strategy
        Document the strategic approach in L2-BEHAVIORS/strategic/
        """)
        
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Strategy: {block.text[:100]}...")
        
        # Phase 2: Tactical Response (simulated market feedback)
        print("\n--- PHASE 2: Tactical Response ---")
        await client.query("""
        @tactics: Analyze market response (simulated)
        Assume we received:
        - 100 customer responses
        - 60% positive, 40% cited complexity
        - Avg satisfaction: 7/10
        
        Document findings in L2-BEHAVIORS/tactical/
        """)
        
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Tactics: {block.text[:100]}...")
        
        # Phase 3: Belief Validation
        print("\n--- PHASE 3: Belief Validation ---")
        await client.query("""
        @validator: Update beliefs based on tactical findings
        - 60% positive → validate some assumptions
        - 40% complexity concerns → flag for capability update
        - Generate updated belief report
        """)
        
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Validator: {block.text[:100]}...")
        
        # Phase 4: Next Strategy (Informed)
        print("\n--- PHASE 4: Refined Strategy ---")
        await client.query("""
        @strategy: Plan next iteration based on validated beliefs
        Incorporate learnings from tactical analysis
        Use higher-confidence assumptions
        """)
        
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Refined Strategy: {block.text[:100]}...")


def main():
    """Run agent examples"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python agent_example.py <org-directory>")
        print("Example: python agent_example.py ./Example-Org")
        sys.exit(1)
    
    org_path = Path(sys.argv[1])
    
    if not org_path.exists():
        print(f"Error: {org_path} does not exist")
        print("Create an organization first:")
        print("  bash setup-example.sh Example-Org")
        sys.exit(1)
    
    if not AGENTS_AVAILABLE:
        print("ERROR: claude-agent-sdk not installed")
        print("Install with: pip install claude-agent-sdk")
        sys.exit(1)
    
    # Run examples
    print("Running Dilts Agent Integration Examples")
    print(f"Organization: {org_path}")
    
    asyncio.run(simple_strategic_example(org_path))
    asyncio.run(tactical_feedback_example(org_path))
    asyncio.run(belief_validation_example(org_path))
    asyncio.run(full_learning_cycle_example(org_path))
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("\nCheck the organization directory for agent-generated files:")
    print(f"  - {org_path}/L2-BEHAVIORS/strategic/")
    print(f"  - {org_path}/L2-BEHAVIORS/tactical/")
    print(f"  - {org_path}/L4-BELIEFS/assumptions/")


if __name__ == "__main__":
    main()
