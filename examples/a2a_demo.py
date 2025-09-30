"""
Demo: A2AWalker with graceful pause/resume.

This example demonstrates the key features of A2AWalker:
1. Graceful interruption at any Dilts level
2. WHAT→WHY chain preservation during pause
3. Progress inspection with full provenance
4. Resume from exact position
5. Dynamic re-planning with update_what()

Run this file to see A2A task lifecycle in action:
    python examples/a2a_demo.py
"""

from sixspec.core.models import Dimension, DiltsLevel, W5H1
from sixspec.walkers.a2a_walker import A2AWalker


def demo_basic_pause_resume():
    """Demo: Basic pause and resume workflow."""
    print("\n=== Demo 1: Basic Pause/Resume ===\n")

    # Create walker at Capability level
    walker = A2AWalker(level=DiltsLevel.CAPABILITY)

    # Set dimensional context
    walker.add_context(Dimension.WHAT, "Integrate payment system")
    walker.add_context(Dimension.WHY, "Launch premium tier")

    # Start task
    walker.task.start()
    print(f"Task started: {walker.task.status.value}")

    # Pause execution
    walker.pause()
    print(f"Task paused: {walker.task.status.value}")

    # Context preserved
    print(f"WHAT preserved: {walker.context[Dimension.WHAT]}")
    print(f"WHY preserved: {walker.context[Dimension.WHY]}")

    # Resume execution
    walker.resume()
    print(f"Task resumed: {walker.task.status.value}")


def demo_cascade_pause():
    """Demo: Cascade pause to children."""
    print("\n=== Demo 2: Cascade Pause ===\n")

    # Create parent-child hierarchy
    parent = A2AWalker(level=DiltsLevel.IDENTITY)
    parent.add_context(Dimension.WHAT, "Launch product")
    parent.task.start()
    print(f"Parent started: {parent.task.status.value}")

    # Create children
    child1 = A2AWalker(level=DiltsLevel.BELIEFS, parent=parent)
    child1.add_context(Dimension.WHAT, "Build features")
    child1.add_context(Dimension.WHY, "Launch product")
    child1.task.start()

    child2 = A2AWalker(level=DiltsLevel.BELIEFS, parent=parent)
    child2.add_context(Dimension.WHAT, "Setup infrastructure")
    child2.add_context(Dimension.WHY, "Launch product")
    child2.task.start()

    parent.children = [child1, child2]

    print(f"Child 1 started: {child1.task.status.value}")
    print(f"Child 2 started: {child2.task.status.value}")

    # Pause parent (cascades to children)
    parent.pause()
    print("\nAfter parent pause:")
    print(f"Parent: {parent.task.status.value}")
    print(f"Child 1: {child1.task.status.value}")
    print(f"Child 2: {child2.task.status.value}")


def demo_progress_inspection():
    """Demo: Inspect progress with get_progress()."""
    print("\n=== Demo 3: Progress Inspection ===\n")

    # Create mission walker
    mission = A2AWalker(level=DiltsLevel.MISSION)
    mission.add_context(Dimension.WHAT, "Increase revenue by 20%")
    mission.task.start()

    # Create identity child
    identity = A2AWalker(level=DiltsLevel.IDENTITY, parent=mission)
    identity.add_context(Dimension.WHAT, "Launch premium tier")
    identity.add_context(Dimension.WHY, "Increase revenue by 20%")
    identity.task.start()

    # Create beliefs child
    beliefs = A2AWalker(level=DiltsLevel.BELIEFS, parent=identity)
    beliefs.add_context(Dimension.WHAT, "Build billing system")
    beliefs.add_context(Dimension.WHY, "Launch premium tier")
    beliefs.task.start()

    mission.children = [identity]
    identity.children = [beliefs]

    # Pause for inspection
    mission.pause()

    # Get full progress
    progress = mission.get_progress()
    print("Mission Progress:")
    print(f"  Level: {progress['level']}")
    print(f"  Status: {progress['status']}")
    print(f"  WHAT: {progress['what']}")
    print(f"  Provenance chain: {progress['provenance']}")
    print(f"  Children: {len(progress['children'])}")

    # Inspect child progress
    if progress['children']:
        child_progress = progress['children'][0]
        print(f"\nChild Progress:")
        print(f"  Level: {child_progress['level']}")
        print(f"  WHAT: {child_progress['what']}")
        print(f"  WHY: {child_progress['why']}")


def demo_dynamic_replanning():
    """Demo: Update WHAT while preserving WHY."""
    print("\n=== Demo 4: Dynamic Re-planning ===\n")

    walker = A2AWalker(level=DiltsLevel.CAPABILITY)
    walker.add_context(Dimension.WHAT, "Use Stripe for payments")
    walker.add_context(Dimension.WHY, "Process customer payments")
    walker.task.start()

    print(f"Original WHAT: {walker.context[Dimension.WHAT]}")
    print(f"WHY: {walker.context[Dimension.WHY]}")

    # Pause and realize we need different approach
    walker.pause()

    # Update WHAT while preserving WHY
    walker.update_what("Use PayPal for payments")

    print(f"\nUpdated WHAT: {walker.context[Dimension.WHAT]}")
    print(f"WHY preserved: {walker.context[Dimension.WHY]}")

    # Resume with new approach
    walker.resume()
    print(f"Resumed with new approach: {walker.task.status.value}")


def demo_provenance_tracing():
    """Demo: Trace full WHAT→WHY chain."""
    print("\n=== Demo 5: Provenance Tracing ===\n")

    # Create 4-level hierarchy
    L6 = A2AWalker(level=DiltsLevel.MISSION)
    L6.add_context(Dimension.WHAT, "Dominate market")

    L5 = A2AWalker(level=DiltsLevel.IDENTITY, parent=L6)
    L5.add_context(Dimension.WHAT, "Launch premium tier")

    L4 = A2AWalker(level=DiltsLevel.BELIEFS, parent=L5)
    L4.add_context(Dimension.WHAT, "Build subscription billing")

    L3 = A2AWalker(level=DiltsLevel.CAPABILITY, parent=L4)
    L3.add_context(Dimension.WHAT, "Integrate Stripe API")

    # Trace provenance from L3 to L6
    chain = L3.trace_provenance()

    print("Full Provenance Chain (Mission → Capability):")
    for i, what in enumerate(chain, 1):
        print(f"  L{7-i}: {what}")

    print("\nThis shows the complete WHY chain:")
    print(f"  Why integrate Stripe? → {L3.context.get(Dimension.WHY)}")


def demo_status_streaming():
    """Demo: Stream status updates."""
    print("\n=== Demo 6: Status Streaming ===\n")

    walker = A2AWalker(level=DiltsLevel.CAPABILITY)
    walker.add_context(Dimension.WHAT, "Deploy application")
    walker.task.start()

    print("Streaming status updates:")

    # Get 3 status updates
    stream = walker.stream_status()
    for i in range(3):
        try:
            status = next(stream)
            print(f"  Update {i+1}: Status={status['status']}, Progress={status['progress_pct']:.1f}%")
        except StopIteration:
            break

    walker.task.complete("Deployed successfully")
    print(f"\nFinal status: {walker.task.status.value}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("A2AWalker Demo: Graceful Interruption & Task Lifecycle")
    print("="*60)

    try:
        demo_basic_pause_resume()
        demo_cascade_pause()
        demo_progress_inspection()
        demo_dynamic_replanning()
        demo_provenance_tracing()
        demo_status_streaming()

        print("\n" + "="*60)
        print("All demos completed successfully!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\nError running demo: {e}")
        import traceback
        traceback.print_exc()
