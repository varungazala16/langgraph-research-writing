#!/usr/bin/env python
"""
Quick demo script for the Multi-Agent Research & Writing System.

This script runs a simple demo to verify the installation and showcase
the system's capabilities.
"""

import os
import sys
from dotenv import load_dotenv


def check_setup():
    """Check if the system is properly set up."""
    print("\n" + "="*60)
    print("🔧 Checking System Setup")
    print("="*60)
    
    # Load environment
    load_dotenv()
    
    # Check Python version
    py_version = sys.version_info
    print(f"\n✓ Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 9):
        print("❌ Python 3.9+ required")
        return False
    
    # Check dependencies
    try:
        import langgraph
        import langchain
        import langchain_openai
        import langchain_community
        print("✓ All dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    if openai_key:
        print(f"✓ OpenAI API key found ({openai_key[:8]}...)")
    else:
        print("❌ OpenAI API key not found")
        print("   Set OPENAI_API_KEY in .env file")
        return False
    
    if tavily_key:
        print(f"✓ Tavily API key found ({tavily_key[:8]}...)")
    else:
        print("❌ Tavily API key not found")
        print("   Set TAVILY_API_KEY in .env file")
        return False
    
    print("\n" + "="*60)
    print("✅ System is ready!")
    print("="*60 + "\n")
    return True


def run_simple_demo():
    """Run a simple demonstration query."""
    from src.workflow import run_workflow
    
    print("\n" + "="*60)
    print("🚀 Running Demo Query")
    print("="*60)
    print("\nQuery: 'What is artificial intelligence?'\n")
    
    try:
        result = run_workflow(
            "What is artificial intelligence?",
            verbose=True
        )
        
        print("\n" + "="*60)
        print("📝 DEMO OUTPUT")
        print("="*60)
        print(f"\n{result['draft_text']}\n")
        print("="*60)
        
        print("\n✅ Demo completed successfully!")
        print("\nNext steps:")
        print("  • Run custom queries: python -m src.main 'your query'")
        print("  • Try interactive mode: python -m src.main --interactive")
        print("  • Explore examples: python examples/example_queries.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        return False


def main():
    """Main entry point."""
    print("\n" + "🤖 "*20)
    print("Multi-Agent Research & Writing System - Demo")
    print("🤖 "*20)
    
    # Check setup
    if not check_setup():
        print("\n⚠️ Please fix the setup issues and try again.\n")
        sys.exit(1)
    
    # Ask user if they want to run demo
    response = input("\n👉 Run a demo query? (y/n): ").strip().lower()
    
    if response in ['y', 'yes']:
        success = run_simple_demo()
        sys.exit(0 if success else 1)
    else:
        print("\n👋 No problem! You can run the demo anytime with:")
        print("   python run_demo.py")
        print("\nOr start using the system:")
        print("   python -m src.main 'your query here'")
        print("\n")
        sys.exit(0)


if __name__ == "__main__":
    main()

