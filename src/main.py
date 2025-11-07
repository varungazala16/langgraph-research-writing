"""Command-line interface for the multi-agent system.

This module provides a CLI for interacting with the LangGraph
multi-agent research and writing system.
"""

import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from src.workflow import run_workflow


def check_environment() -> bool:
    """Check if required environment variables are set.
    
    Returns:
        True if all required variables are present, False otherwise
    """
    required_vars = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please set these in your .env file or environment")
        print("   See .env.template for an example")
        return False
    
    return True


def display_results(state: dict) -> None:
    """Display the results in a formatted way.
    
    Args:
        state: Final workflow state
    """
    print("\n" + "="*60)
    print("📊 WORKFLOW SUMMARY")
    print("="*60)
    
    print(f"\n🎯 Task Type: {state.get('task_type', 'unknown').upper()}")
    print(f"🔄 Iterations: {state.get('iteration', 0)}")
    
    # Display research facts
    facts = state.get('gathered_facts', [])
    if facts:
        print(f"\n🔍 Research Facts Gathered ({len(facts)}):")
        print("-" * 60)
        for idx, fact in enumerate(facts, 1):
            # Clean up fact display
            fact_text = fact.replace("Source ", "").strip()
            if fact_text.startswith(str(idx)):
                fact_text = fact_text[len(str(idx)):].strip(": ")
            print(f"  {idx}. {fact_text[:200]}{'...' if len(fact_text) > 200 else ''}")
    
    # Display final output
    draft = state.get('draft_text', '')
    if draft:
        print("\n" + "="*60)
        print("📝 FINAL OUTPUT")
        print("="*60)
        print(f"\n{draft}\n")
        print("="*60)
    else:
        print("\n⚠️ No output generated")


def interactive_mode():
    """Run the system in interactive mode."""
    print("\n" + "="*60)
    print("🤖 Multi-Agent Research & Writing System")
    print("="*60)
    print("\nInteractive Mode - Type 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            query = input("💬 Enter your query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if not query:
                print("⚠️ Please enter a valid query\n")
                continue
            
            # Run the workflow
            result = run_workflow(query, verbose=True)
            display_results(result)
            
            print("\n" + "-"*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent Research & Writing System powered by LangGraph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single query mode
  python -m src.main "What are the latest developments in quantum computing?"
  
  # Interactive mode
  python -m src.main --interactive
  
  # Quiet mode (only output)
  python -m src.main --quiet "Research AI safety and write a report"
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="The query to process (omit for interactive mode)"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output, show only final result"
    )
    
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Don't show workflow summary, only final output"
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Determine mode
    if args.interactive or (not args.query):
        interactive_mode()
    else:
        # Single query mode
        try:
            result = run_workflow(args.query, verbose=not args.quiet)
            
            if args.no_summary:
                # Only print the final output
                print(result.get('draft_text', ''))
            else:
                display_results(result)
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            sys.exit(1)


if __name__ == "__main__":
    main()

