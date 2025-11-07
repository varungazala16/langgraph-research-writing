"""LangGraph Workflow Definition.

This module defines the stateful workflow graph that orchestrates
the multi-agent system using LangGraph.
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents.supervisor import supervisor_node
from src.agents.research_agent import research_node
from src.agents.writing_agent import writing_node


def route_supervisor(state: AgentState) -> Literal["research", "writing", "__end__"]:
    """Conditional routing function for supervisor decisions.
    
    This function reads the next_agent field from state and routes
    the workflow to the appropriate next node.
    
    Args:
        state: Current workflow state
        
    Returns:
        Next node name or END signal
    """
    next_agent = state.get("next_agent", "END")
    
    if next_agent == "research":
        return "research"
    elif next_agent == "writing":
        return "writing"
    elif next_agent == "END":
        return "__end__"
    else:
        # Default to END for unknown states
        return "__end__"


def create_workflow() -> StateGraph:
    """Create and compile the LangGraph workflow.
    
    The workflow structure:
    1. START → supervisor
    2. supervisor → (conditional routing)
       - If research needed → research → supervisor (loop back)
       - If writing needed → writing → END
       - If complete → END
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize the graph with our state schema
    workflow = StateGraph(AgentState)
    
    # Add agent nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("research", research_node)
    workflow.add_node("writing", writing_node)
    
    # Set entry point
    workflow.set_entry_point("supervisor")
    
    # Add conditional edges from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "research": "research",
            "writing": "writing",
            "__end__": END
        }
    )
    
    # Research agent always returns to supervisor for next decision
    workflow.add_edge("research", "supervisor")
    
    # Writing agent goes to END (workflow complete)
    workflow.add_edge("writing", END)
    
    # Compile the graph
    compiled_workflow = workflow.compile()
    
    return compiled_workflow


def run_workflow(user_query: str, verbose: bool = True) -> AgentState:
    """Execute the workflow with a user query.
    
    Args:
        user_query: The user's input query
        verbose: Whether to print progress information
        
    Returns:
        Final state after workflow completion
    """
    if verbose:
        print("\n" + "="*60)
        print("🚀 Starting Multi-Agent Workflow")
        print("="*60)
        print(f"\n📝 Query: {user_query}\n")
    
    # Create initial state
    initial_state: AgentState = {
        "user_query": user_query,
        "task_type": "unknown",
        "gathered_facts": [],
        "draft_text": "",
        "next_agent": "supervisor",
        "messages": [],
        "iteration": 0
    }
    
    # Create and run workflow
    workflow = create_workflow()
    final_state = workflow.invoke(initial_state)
    
    if verbose:
        print("\n" + "="*60)
        print("✅ Workflow Complete")
        print("="*60)
        print(f"\n📊 Total Iterations: {final_state.get('iteration', 0)}")
        print(f"📋 Task Type: {final_state.get('task_type', 'unknown')}")
        print(f"🔍 Facts Gathered: {len(final_state.get('gathered_facts', []))}")
        print(f"📄 Draft Length: {len(final_state.get('draft_text', ''))} characters")
        print("\n" + "="*60 + "\n")
    
    return final_state


if __name__ == "__main__":
    # Test the workflow
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Example test query
    test_query = "What are the latest developments in quantum computing?"
    result = run_workflow(test_query)
    
    print("\n📝 FINAL OUTPUT:")
    print("-" * 60)
    print(result["draft_text"])
    print("-" * 60)

