"""Example queries demonstrating the multi-agent workflow.

This module contains example queries and functions to demonstrate
different workflows and capabilities of the system.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.workflow import run_workflow
from dotenv import load_dotenv


def example_1_pure_research():
    """Example 1: Pure research query requiring web search.
    
    This demonstrates:
    - Supervisor routing to research agent
    - Research agent gathering facts from web
    - Supervisor routing to writing agent
    - Writing agent synthesizing research into content
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Pure Research Query")
    print("="*80)
    print("\nScenario: User asks about recent developments requiring web research")
    print("Expected Flow: Supervisor → Research → Supervisor → Writing → END\n")
    
    query = "What are the latest developments in quantum computing?"
    
    result = run_workflow(query, verbose=True)
    
    print("\n📝 FINAL OUTPUT:")
    print("-" * 80)
    print(result["draft_text"])
    print("-" * 80)
    
    return result


def example_2_writing_with_context():
    """Example 2: Writing task that benefits from research.
    
    This demonstrates:
    - Supervisor recognizing need for research before writing
    - Research gathering context and data
    - Writing creating comprehensive summary
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Writing Task with Research Context")
    print("="*80)
    print("\nScenario: User requests written content that requires factual research")
    print("Expected Flow: Supervisor → Research → Supervisor → Writing → END\n")
    
    query = "Write a summary of the current state of fusion energy research"
    
    result = run_workflow(query, verbose=True)
    
    print("\n📝 FINAL OUTPUT:")
    print("-" * 80)
    print(result["draft_text"])
    print("-" * 80)
    
    return result


def example_3_combined_workflow():
    """Example 3: Explicit combined research and writing task.
    
    This demonstrates:
    - Clear multi-step workflow
    - Research phase gathering comprehensive information
    - Writing phase creating structured report
    - Full supervisor orchestration
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Combined Research & Writing Workflow")
    print("="*80)
    print("\nScenario: User explicitly requests research followed by report writing")
    print("Expected Flow: Supervisor → Research → Supervisor → Writing → END\n")
    
    query = "Research the key challenges in AI safety and write a brief report"
    
    result = run_workflow(query, verbose=True)
    
    print("\n📝 FINAL OUTPUT:")
    print("-" * 80)
    print(result["draft_text"])
    print("-" * 80)
    
    return result


def example_4_direct_writing():
    """Example 4: Simple writing task without research.
    
    This demonstrates:
    - Supervisor recognizing no research needed
    - Direct routing to writing agent
    - Faster workflow for creative tasks
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Direct Writing (No Research)")
    print("="*80)
    print("\nScenario: Creative writing task that doesn't require web research")
    print("Expected Flow: Supervisor → Writing → END\n")
    
    query = "Write a motivational paragraph about the importance of continuous learning"
    
    result = run_workflow(query, verbose=True)
    
    print("\n📝 FINAL OUTPUT:")
    print("-" * 80)
    print(result["draft_text"])
    print("-" * 80)
    
    return result


def run_all_examples():
    """Run all example queries sequentially."""
    print("\n" + "🎬 "*20)
    print("RUNNING ALL EXAMPLE QUERIES")
    print("🎬 "*20)
    
    examples = [
        ("Example 1: Pure Research Query", example_1_pure_research),
        ("Example 2: Writing with Context", example_2_writing_with_context),
        ("Example 3: Combined Workflow", example_3_combined_workflow),
        ("Example 4: Direct Writing", example_4_direct_writing)
    ]
    
    results = {}
    
    for name, example_func in examples:
        try:
            print(f"\n\n{'='*80}")
            print(f"Running: {name}")
            print(f"{'='*80}")
            result = example_func()
            results[name] = {
                "success": True,
                "result": result
            }
            input("\n⏸️  Press Enter to continue to next example...")
        except Exception as e:
            print(f"\n❌ Error in {name}: {str(e)}")
            results[name] = {
                "success": False,
                "error": str(e)
            }
    
    # Summary
    print("\n" + "="*80)
    print("📊 EXAMPLES SUMMARY")
    print("="*80)
    
    for name, result in results.items():
        status = "✅ Success" if result["success"] else "❌ Failed"
        print(f"{status}: {name}")
        if not result["success"]:
            print(f"   Error: {result['error']}")
    
    print("\n" + "="*80 + "\n")


def interactive_demo():
    """Interactive demo allowing user to choose examples."""
    print("\n" + "="*80)
    print("🤖 Multi-Agent System - Interactive Demo")
    print("="*80)
    
    print("\nAvailable Examples:")
    print("  1. Pure Research Query (quantum computing)")
    print("  2. Writing with Research Context (fusion energy)")
    print("  3. Combined Research & Writing (AI safety report)")
    print("  4. Direct Writing (motivational content)")
    print("  5. Run all examples")
    print("  0. Exit")
    
    while True:
        try:
            choice = input("\n👉 Select an example (0-5): ").strip()
            
            if choice == "0":
                print("\n👋 Goodbye!\n")
                break
            elif choice == "1":
                example_1_pure_research()
            elif choice == "2":
                example_2_writing_with_context()
            elif choice == "3":
                example_3_combined_workflow()
            elif choice == "4":
                example_4_direct_writing()
            elif choice == "5":
                run_all_examples()
            else:
                print("⚠️ Invalid choice. Please select 0-5.")
                continue
            
            print("\n" + "-"*80)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


def main():
    """Main entry point for examples."""
    # Load environment variables
    load_dotenv()
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        print("\n❌ Error: Missing API keys!")
        print("Please set OPENAI_API_KEY and TAVILY_API_KEY in your .env file")
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ["1", "example1"]:
            example_1_pure_research()
        elif arg in ["2", "example2"]:
            example_2_writing_with_context()
        elif arg in ["3", "example3"]:
            example_3_combined_workflow()
        elif arg in ["4", "example4"]:
            example_4_direct_writing()
        elif arg in ["all", "run-all"]:
            run_all_examples()
        else:
            print(f"Unknown argument: {arg}")
            print("Usage: python example_queries.py [1|2|3|4|all]")
    else:
        # Interactive mode
        interactive_demo()


if __name__ == "__main__":
    main()

