"""State model for the multi-agent workflow.

This module defines the shared state structure that persists across
all agent transitions in the LangGraph workflow.
"""

from typing import TypedDict, Annotated, List
from langgraph.graph import add_messages


class AgentState(TypedDict):
    """State object shared across all agents in the workflow.
    
    Attributes:
        user_query: The original user request/query
        task_type: Classification of the task ("research", "writing", or "unknown")
        gathered_facts: List of research findings collected by research agent
        draft_text: Final written output from writing agent
        next_agent: Routing decision for which agent to call next
        messages: Conversation history with LLM messages
        iteration: Counter tracking workflow steps for debugging
    """
    user_query: str
    task_type: str
    gathered_facts: List[str]
    draft_text: str
    next_agent: str
    messages: Annotated[List, add_messages]
    iteration: int


def create_initial_state(user_query: str) -> AgentState:
    """Create an initial state object for a new workflow run.
    
    Args:
        user_query: The user's input query
        
    Returns:
        AgentState: Initial state with default values
    """
    return {
        "user_query": user_query,
        "task_type": "unknown",
        "gathered_facts": [],
        "draft_text": "",
        "next_agent": "supervisor",
        "messages": [],
        "iteration": 0
    }

