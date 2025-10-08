#!/usr/bin/env python3
"""
SixSpec Demo for Anthropic
===========================

This script demonstrates the core capabilities of SixSpec:
1. Dimensional commit parsing with WHY + HOW
2. Queryable Git history by purpose
3. WHAT→WHY provenance chains through Dilts hierarchy
4. Auto-organization via hypergraph clustering

Run this to see SixSpec in action!
"""

import sys
from pathlib import Path

# Add sixspec to path
sys.path.insert(0, str(Path(__file__).parent))

from sixspec.core.models import Chunk, Dimension, DiltsLevel
from sixspec.git.parser import CommitMessageParser
from sixspec.walkers.dilts_walker import DiltsWalker, ValidationResult
from sixspec.core.hypergraph import SpecificationHypergraph


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_1_commit_parsing():
    """Demo 1: Parse dimensional commits."""
    print_section("DEMO 1: Dimensional Commit Messages")
    
    print("Traditional commit:")
    print('  git commit -m "fix: payment timeout"\n')
    print("❌ Problem: No context! WHY did timeout happen? HOW was it fixed?\n")
    
    print("SixSpec dimensional commit:")
    commit_msg = """fix: payment timeout

WHY: Users abandoning carts at 25% rate due to API timeout
HOW: Added retry logic with exponential backoff (3 attempts)
WHERE: src/payment/stripe_integration.py"""
    
    print(f'  {commit_msg.replace(chr(10), chr(10) + "  ")}\n')
    
    # Parse it
    commit = CommitMessageParser.parse(commit_msg, "abc123")
    
    print("✅ Parsed commit:")
    print(f"  Type:  {commit.commit_type}")
    print(f"  Hash:  {commit.commit_hash}")
    print(f"  WHY:   {commit.need(Dimension.WHY)}")
    print(f"  HOW:   {commit.need(Dimension.HOW)}")
    print(f"  WHERE: {commit.need(Dimension.WHERE)}")
    
    print("\n💡 Key Point: Git history now captures PURPOSE, not just changes")


def demo_2_queryable_history():
    """Demo 2: Query commits by dimension."""
    print_section("DEMO 2: Queryable Git History")
    
    # Create example commits
    commits = [
        """fix: payment timeout

WHY: Users abandoning carts at 25% rate
HOW: Added retry logic with exponential backoff
WHERE: src/payment/stripe.py""",
        
        """feat: add search filters

WHY: Users cannot find products efficiently
HOW: Implemented faceted search with Elasticsearch
WHERE: src/search/api.py""",
        
        """fix: search performance

WHY: Search taking 5+ seconds with large catalog
HOW: Added database indices and query optimization
WHERE: src/search/database.py"""
    ]
    
    parsed = [CommitMessageParser.parse(msg, f"hash{i}") for i, msg in enumerate(commits)]
    
    print("Created 3 example commits:")
    for c in parsed:
        print(f"  • {c.commit_type}: {c.object}")
    
    print("\n📊 Query Examples:\n")
    
    # Query 1: By file location
    print("1. Find all commits affecting payment code:")
    print('   query(where="payment")')
    payment_commits = [c for c in parsed if c.need(Dimension.WHERE) 
                      and "payment" in c.need(Dimension.WHERE).lower()]
    for c in payment_commits:
        print(f"     → {c.object}: {c.need(Dimension.WHY)}")
    
    # Query 2: By purpose
    print("\n2. Find all user experience improvements:")
    print('   query(why="users")')
    ux_commits = [c for c in parsed if "users" in c.need(Dimension.WHY).lower()]
    for c in ux_commits:
        print(f"     → {c.object}: {c.need(Dimension.WHY)}")
    
    # Query 3: By type
    print("\n3. Find all bug fixes:")
    print('   query(commit_type="fix")')
    fixes = [c for c in parsed if c.commit_type == "fix"]
    for c in fixes:
        print(f"     → {c.object}: {c.need(Dimension.HOW)}")
    
    print("\n💡 Key Point: Search by PURPOSE and APPROACH, not just file names")


def demo_3_provenance_chain():
    """Demo 3: WHAT→WHY propagation through Dilts hierarchy."""
    print_section("DEMO 3: Provenance Chain - WHAT→WHY Propagation")
    
    print("Hierarchical delegation with purpose propagation:")
    print("  Parent's WHAT becomes child's WHY\n")
    
    # Create a concrete walker that implements the abstract methods
    class ConcreteWalker(DiltsWalker):
        def generate_strategies(self, spec, n):
            base = spec.need(Dimension.WHAT) or "achieve goal"
            return [f"{base} - Approach {i+1}" for i in range(n)]
        
        def validate(self, result):
            return ValidationResult(
                score=0.85 if result else 0.0,
                passed=bool(result),
                details="Demo validation"
            )
    
    # Mission level
    mission = ConcreteWalker(level=DiltsLevel.MISSION)
    mission_spec = Chunk(
        subject="Company",
        predicate="needs",
        object="market leadership",
        dimensions={
            Dimension.WHAT: "Achieve market leadership in payments"
        }
    )
    
    print("Level 6 (Mission):")
    print(f"  WHAT: {mission_spec.need(Dimension.WHAT)}")
    
    # Execute to create delegation chain
    mission.execute(mission_spec)
    
    # Walk down the chain
    walker = mission
    level = 6
    print()
    
    while walker.children:
        walker = walker.children[0]
        level -= 1
        
        what = walker.context.get(Dimension.WHAT, "")
        why = walker.context.get(Dimension.WHY, "")
        
        print(f"Level {level} ({walker.level.name}):")
        print(f"  WHY:  {why}")
        if what:
            print(f"  WHAT: {what}")
        print()
    
    # Show full provenance
    print("Full provenance chain:")
    provenance = walker.trace_provenance()
    for i, purpose in enumerate(provenance):
        print(f"  L{6-i}: {purpose}")
    
    print("\n💡 Key Point: Every action traces back to business mission")
    print("   Ask 'why does this code exist?' → follow the chain!")


def demo_4_hypergraph():
    """Demo 4: Auto-organization via hypergraph."""
    print_section("DEMO 4: Hypergraph Auto-Organization")
    
    print("The 'Grocery Store Rule': specs sharing ≥1 dimension cluster together\n")
    
    graph = SpecificationHypergraph()
    
    # Today's errands
    milk = Chunk("User", "buys", "milk",
        dimensions={Dimension.WHERE: "grocery", Dimension.WHEN: "today"})
    bread = Chunk("User", "buys", "bread", 
        dimensions={Dimension.WHERE: "grocery", Dimension.WHEN: "today"})
    hammer = Chunk("User", "buys", "hammer",
        dimensions={Dimension.WHERE: "hardware", Dimension.WHEN: "today"})
    
    print("Adding 3 tasks:")
    print(f"  • Buy milk   (WHERE: grocery, WHEN: today)")
    print(f"  • Buy bread  (WHERE: grocery, WHEN: today)")
    print(f"  • Buy hammer (WHERE: hardware, WHEN: today)")
    
    graph.add_object(milk)
    graph.add_object(bread)
    graph.add_object(hammer)
    
    print("\n📊 Auto-detected clusters:")
    clusters = graph.find_clusters()
    for i, cluster in enumerate(clusters, 1):
        print(f"  Cluster {i}:")
        for node_id in cluster:
            obj = graph._object_map[node_id]
            print(f"    • {obj.object}")
    
    print("\n🏗️  Auto-generated hierarchy:")
    hierarchy = graph.organize_hierarchy()
    
    def print_hierarchy(node, indent=0):
        prefix = "  " * indent
        if node.level == "epic":
            print(f"{prefix}📚 Epic: {node.name}")
        elif node.level == "story":
            print(f"{prefix}  📖 Story: {node.name}")
        elif node.level == "task":
            print(f"{prefix}    ✓ Task: {node.name}")
        
        for child in node.children:
            if hasattr(child, 'level'):
                print_hierarchy(child, indent)
    
    for epic in hierarchy.children:
        print_hierarchy(epic)
    
    print("\n💡 Key Point: No manual organization needed!")
    print("   Specs self-cluster based on shared context")


def demo_summary():
    """Print summary of capabilities."""
    print_section("SUMMARY: What SixSpec Enables")
    
    print("✅ Dimensional Commits")
    print("   • Git commits capture WHY and HOW, not just WHAT")
    print("   • Git hook enforces structure at commit time")
    print("   • History becomes queryable documentation\n")
    
    print("✅ Queryable Git History")
    print("   • Search by purpose, not just files")
    print("   • 'Show me all timeout fixes'")
    print("   • 'Why does this file exist?'\n")
    
    print("✅ Provenance Chains")
    print("   • WHAT→WHY propagation from mission to implementation")
    print("   • Every line of code traces to business value")
    print("   • Explainable AI: 'Why did you do that?'\n")
    
    print("✅ Auto-Organization")
    print("   • Specs cluster by shared dimensions")
    print("   • No manual epic/story creation")
    print("   • Emergent structure from context\n")
    
    print("🎯 Perfect For:")
    print("   • AI agents understanding codebase evolution")
    print("   • Developers asking 'why does this exist?'")
    print("   • Impact analysis across purpose domains")
    print("   • Self-documenting systems")
    
    print("\n" + "=" * 70)
    print("  Explore the code: /home/Projects/SixSpec")
    print("  Read the docs:   README.md, ARCHITECTURE.md, DESIGN_PHILOSOPHY.md")
    print("=" * 70)


def main():
    """Run all demos."""
    print("\n" + "█" * 70)
    print("  SixSpec: Dimensional Specifications with Purpose Propagation")
    print("  Demo for Anthropic")
    print("█" * 70)
    
    try:
        demo_1_commit_parsing()
        input("\n[Press Enter to continue to Demo 2...]")
        
        demo_2_queryable_history()
        input("\n[Press Enter to continue to Demo 3...]")
        
        demo_3_provenance_chain()
        input("\n[Press Enter to continue to Demo 4...]")
        
        demo_4_hypergraph()
        input("\n[Press Enter to see summary...]")
        
        demo_summary()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Thanks for watching!")
        sys.exit(0)


if __name__ == "__main__":
    main()
