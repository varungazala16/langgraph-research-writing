"""Supervisor Agent implementation.

This agent coordinates the workflow by analyzing the current state
and routing tasks to the appropriate specialized agent.
"""

from typing import Dict, Any, Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import os


class RouteDecision(BaseModel):
    """Structured output for supervisor routing decisions."""
    
    next_agent: Literal["research", "writing", "END"] = Field(
        description="The next agent to call: 'research' for gathering information, 'writing' for creating content, or 'END' if complete"
    )
    reasoning: str = Field(
        description="Brief explanation of why this agent was chosen"
    )
    task_type: Literal["research", "writing", "combined", "complete"] = Field(
        description="Classification of the current task"
    )


def supervisor_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Supervisor agent that routes tasks to appropriate agents.
    
    The supervisor analyzes the user query and current state to determine
    the next step in the workflow. Decision logic:
    - If no facts gathered yet → route to research
    - If facts present but no draft → route to writing  
    - If draft complete → END
    - Can also decide to skip research for simple writing tasks
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with next_agent and task_type set
    """
    print("\n🎯 Supervisor: Analyzing task and routing...")
    
    user_query = state["user_query"]
    gathered_facts = state.get("gathered_facts", [])
    draft_text = state.get("draft_text", "")
    iteration = state.get("iteration", 0) + 1
    
    # Check if workflow is complete
    if draft_text and draft_text != "":
        print("🎯 Supervisor: Work complete, ending workflow")
        return {
            **state,
            "next_agent": "END",
            "task_type": "complete",
            "iteration": iteration
        }
    
    try:
        # Initialize OpenAI LLM with structured output
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Create supervisor prompt
        supervisor_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a supervisor coordinating a team of specialized agents.
Your team consists of:
1. Research Agent - Gathers information from web searches
2. Writing Agent - Creates written content based on research or general knowledge

Analyze the user's query and current workflow state to decide the next step.

Decision Guidelines:
- If the query requires factual information or recent data → route to 'research' first
- If research has been completed (facts gathered) → route to 'writing'
- If the query is a simple creative/writing task without need for research → route directly to 'writing'
- If writing is complete → route to 'END'

Current State:
- Research Facts Gathered: {has_facts}
- Draft Written: {has_draft}
- Number of Facts: {num_facts}
"""),
            ("user", "User Query: {query}\n\nWhat should be the next agent to call?")
        ])
        
        # Bind structured output to LLM
        structured_llm = llm.with_structured_output(RouteDecision)
        chain = supervisor_prompt | structured_llm
        
        # Get routing decision
        decision = chain.invoke({
            "query": user_query,
            "has_facts": "Yes" if gathered_facts else "No",
            "has_draft": "Yes" if draft_text else "No",
            "num_facts": len(gathered_facts)
        })
        
        print(f"🎯 Supervisor: Decision → {decision.next_agent}")
        print(f"🎯 Supervisor: Reasoning → {decision.reasoning}")
        
        return {
            **state,
            "next_agent": decision.next_agent,
            "task_type": decision.task_type,
            "iteration": iteration,
            "messages": state.get("messages", []) + [
                {"role": "assistant", "content": f"Supervisor routing to {decision.next_agent}: {decision.reasoning}"}
            ]
        }
        
    except Exception as e:
        print(f"⚠️ Supervisor: Error during routing: {str(e)}")
        # Default fallback logic
        if not gathered_facts:
            next_agent = "research"
        elif not draft_text:
            next_agent = "writing"
        else:
            next_agent = "END"
            
        print(f"🎯 Supervisor: Using fallback routing → {next_agent}")
        
        return {
            **state,
            "next_agent": next_agent,
            "task_type": "unknown",
            "iteration": iteration,
            "messages": state.get("messages", []) + [
                {"role": "assistant", "content": f"Supervisor using fallback routing to {next_agent}"}
            ]
        }

