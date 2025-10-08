"""
Claude Walker Demo: Hierarchical execution with Claude Agent SDK

This example demonstrates the ClaudeWalker implementation using the
Claude Agent SDK for pause/resume and hierarchical task execution.

Features demonstrated:
- Creating walkers at different Dilts levels
- WHAT→WHY purpose propagation
- Session management and pause/resume
- Progress tracking with full provenance
- Subagent coordination

Usage:
    python examples/claude_walker_demo.py
"""

import asyncio
from sixspec.walkers import ClaudeWalker
from sixspec.core.models import Dimension, DiltsLevel, Chunk


async def demo_basic_execution():
    """Demonstrate basic ClaudeWalker execution."""
    print("=" * 60)
    print("DEMO 1: Basic Execution")
    print("=" * 60)

    # Create walker at CAPABILITY level (most common starting point)
    walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)

    # Create a spec with WHAT dimension
    spec = Chunk(
        subject="System",
        predicate="needs",
        object="payment integration",
        dimensions={
            Dimension.WHAT: "Integrate Stripe payment processing"
        }
    )

    print(f"\n📋 Executing spec at {walker.level.name} level")
    print(f"   WHAT: {spec.need(Dimension.WHAT)}")

    try:
        result = await walker.execute(spec)
        print(f"\n✅ Execution completed!")
        print(f"   Session ID: {walker.session_id}")
        print(f"   Result: {result}")
    except Exception as e:
        print(f"\n❌ Execution failed: {e}")

    print()


async def demo_what_why_propagation():
    """Demonstrate WHAT→WHY propagation through levels."""
    print("=" * 60)
    print("DEMO 2: WHAT→WHY Propagation")
    print("=" * 60)

    # Create parent walker
    parent = ClaudeWalker(level=DiltsLevel.IDENTITY)
    parent_spec = Chunk(
        subject="Company",
        predicate="wants to be",
        object="market leader",
        dimensions={
            Dimension.WHAT: "Become the leading payment platform"
        }
    )

    print(f"\n👤 Parent ({parent.level.name}):")
    print(f"   WHAT: {parent_spec.need(Dimension.WHAT)}")

    # Set up parent context
    parent.current_node = parent_spec
    parent.add_context(Dimension.WHAT, parent_spec.need(Dimension.WHAT))

    # Create child walker - inherits parent's WHAT as WHY
    child = ClaudeWalker(level=DiltsLevel.BELIEFS, parent=parent)
    child_spec = Chunk(
        subject="Team",
        predicate="believes in",
        object="quality",
        dimensions={
            Dimension.WHAT: "Focus on developer experience"
        }
    )

    print(f"\n👶 Child ({child.level.name}):")
    print(f"   WHY: {child.context.get(Dimension.WHY)} (inherited from parent)")
    print(f"   WHAT: {child_spec.need(Dimension.WHAT)}")

    # Create grandchild - inherits child's WHAT as WHY
    child.current_node = child_spec
    child.add_context(Dimension.WHAT, child_spec.need(Dimension.WHAT))

    grandchild = ClaudeWalker(level=DiltsLevel.CAPABILITY, parent=child)
    grandchild_spec = Chunk(
        subject="Engineers",
        predicate="implement",
        object="SDK",
        dimensions={
            Dimension.WHAT: "Build comprehensive API documentation"
        }
    )

    print(f"\n👶👶 Grandchild ({grandchild.level.name}):")
    print(f"   WHY: {grandchild.context.get(Dimension.WHY)} (inherited from child)")
    print(f"   WHAT: {grandchild_spec.need(Dimension.WHAT)}")

    # Trace full provenance chain
    grandchild.current_node = grandchild_spec
    grandchild.add_context(Dimension.WHAT, grandchild_spec.need(Dimension.WHAT))

    chain = grandchild.trace_provenance()
    print(f"\n🔍 Full Provenance Chain:")
    for i, what in enumerate(chain, 1):
        print(f"   {i}. {what}")

    print()


async def demo_pause_resume():
    """Demonstrate pause/resume functionality."""
    print("=" * 60)
    print("DEMO 3: Pause and Resume")
    print("=" * 60)

    walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
    spec = Chunk(
        subject="System",
        predicate="needs",
        object="database",
        dimensions={
            Dimension.WHAT: "Migrate database to PostgreSQL"
        }
    )

    print(f"\n📋 Starting execution...")
    print(f"   WHAT: {spec.need(Dimension.WHAT)}")

    try:
        # Start execution
        asyncio.create_task(walker.execute(spec))

        # Wait a bit, then pause
        await asyncio.sleep(0.1)
        print(f"\n⏸️  Pausing execution...")
        session_id = await walker.pause()

        print(f"   Paused at session: {session_id}")
        print(f"   Is paused: {walker.is_paused}")

        # Inspect progress
        progress = walker.get_progress()
        print(f"\n📊 Current Progress:")
        print(f"   Level: {progress['level']} ({DiltsLevel(progress['level']).name})")
        print(f"   Session: {progress['session_id']}")
        print(f"   Paused: {progress['is_paused']}")
        print(f"   WHAT: {progress['what']}")

        # Resume execution
        if session_id:
            print(f"\n▶️  Resuming from session {session_id}...")
            result = await walker.resume(session_id, spec)
            print(f"   ✅ Resumed and completed: {result}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    print()


async def demo_progress_tracking():
    """Demonstrate progress tracking with children."""
    print("=" * 60)
    print("DEMO 4: Progress Tracking")
    print("=" * 60)

    # Create parent with children
    parent = ClaudeWalker(level=DiltsLevel.CAPABILITY)
    parent.add_context(Dimension.WHAT, "Build authentication system")

    child1 = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
    child1.add_context(Dimension.WHAT, "Implement login")
    child1.session_id = "session-child1"

    child2 = ClaudeWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
    child2.add_context(Dimension.WHAT, "Implement registration")
    child2.session_id = "session-child2"

    parent.children = [child1, child2]
    parent.session_id = "session-parent"

    # Get progress
    progress = parent.get_progress()

    print(f"\n📊 Parent Progress:")
    print(f"   Walker: {progress['walker_id']}")
    print(f"   Level: {progress['level']} ({DiltsLevel(progress['level']).name})")
    print(f"   WHAT: {progress['what']}")
    print(f"   Session: {progress['session_id']}")

    print(f"\n   Children: {len(progress['children'])}")
    for i, child_progress in enumerate(progress['children'], 1):
        print(f"\n   Child {i}:")
        print(f"     Level: {child_progress['level']} ({DiltsLevel(child_progress['level']).name})")
        print(f"     WHAT: {child_progress['what']}")
        print(f"     WHY: {child_progress['why']}")
        print(f"     Session: {child_progress['session_id']}")

    print()


async def demo_dynamic_replanning():
    """Demonstrate dynamic re-planning while preserving WHY."""
    print("=" * 60)
    print("DEMO 5: Dynamic Re-planning")
    print("=" * 60)

    walker = ClaudeWalker(level=DiltsLevel.CAPABILITY)
    walker.add_context(Dimension.WHAT, "Use Stripe for payments")
    walker.add_context(Dimension.WHY, "Enable premium subscriptions")

    print(f"\n📋 Initial Plan:")
    print(f"   WHAT: {walker.context[Dimension.WHAT]}")
    print(f"   WHY: {walker.context[Dimension.WHY]}")

    # Change approach while keeping purpose
    print(f"\n🔄 Replanning (changing approach, keeping purpose)...")
    walker.update_what("Use PayPal for payments")

    print(f"\n📋 Updated Plan:")
    print(f"   WHAT: {walker.context[Dimension.WHAT]} ⬅️ Changed")
    print(f"   WHY: {walker.context[Dimension.WHY]} ⬅️ Preserved")

    print()


async def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("ClaudeWalker Demonstration")
    print("Claude Agent SDK Integration")
    print("=" * 60)

    # Note: Some demos require actual Claude SDK connection
    # For testing without SDK, they will show the structure

    await demo_basic_execution()
    await demo_what_why_propagation()
    await demo_pause_resume()
    await demo_progress_tracking()
    await demo_dynamic_replanning()

    print("=" * 60)
    print("All demos completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\n💡 Make sure to install dependencies:")
        print("   pip install -e .")
        print("   pip install claude-agent-sdk")
