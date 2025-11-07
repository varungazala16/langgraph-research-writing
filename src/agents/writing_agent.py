"""Writing Agent implementation.

This agent synthesizes research findings into coherent written content
using OpenAI's LLM.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


def writing_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Writing agent node that synthesizes research into written content.
    
    This agent:
    1. Takes gathered facts from state
    2. Uses LLM to create coherent written content
    3. Updates state with draft_text
    4. Sets next_agent to END to signal completion
    
    Args:
        state: Current workflow state containing gathered_facts
        
    Returns:
        Updated state with draft_text populated
    """
    print("\n✍️ Writing Agent: Starting writing process...")
    
    user_query = state["user_query"]
    gathered_facts = state.get("gathered_facts", [])
    iteration = state.get("iteration", 0) + 1
    
    if not gathered_facts or gathered_facts == []:
        print("✍️ Writing Agent: No research data available, writing from general knowledge")
        facts_text = "No specific research data available."
    else:
        facts_text = "\n".join([f"- {fact}" for fact in gathered_facts])
    
    try:
        # Initialize OpenAI LLM
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Create writing prompt
        writing_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert writer and content creator. 
Your task is to synthesize the provided research facts into a well-structured, 
coherent piece of writing that addresses the user's query.

Guidelines:
- Write in a clear, professional, and engaging style
- Structure your content with proper paragraphs
- Include an introduction and conclusion when appropriate
- Base your writing on the provided facts, but feel free to add context and connections
- Aim for 3-5 paragraphs depending on the complexity of the topic
- If no research facts are available, write from general knowledge while being transparent about limitations
"""),
            ("user", """User Query: {query}

Research Facts:
{facts}

Please write a comprehensive response that addresses the user's query based on the research facts above.""")
        ])
        
        # Generate the written content
        chain = writing_prompt | llm
        response = chain.invoke({
            "query": user_query,
            "facts": facts_text
        })
        
        draft_text = response.content
        
        print(f"✍️ Writing Agent: Generated {len(draft_text)} characters of content")
        
        return {
            **state,
            "draft_text": draft_text,
            "next_agent": "END",
            "iteration": iteration,
            "messages": state.get("messages", []) + [
                {"role": "assistant", "content": "Writing completed successfully."}
            ]
        }
        
    except Exception as e:
        print(f"⚠️ Writing Agent: Error during writing: {str(e)}")
        return {
            **state,
            "draft_text": f"Error generating written content: {str(e)}",
            "next_agent": "END",
            "iteration": iteration,
            "messages": state.get("messages", []) + [
                {"role": "assistant", "content": f"Writing encountered an error: {str(e)}"}
            ]
        }

