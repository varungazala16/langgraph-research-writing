"""Research Agent implementation.

This agent performs web searches and gathers information using
LangChain's Tavily search integration.
"""

from typing import Dict, Any
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


def research_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Research agent node that performs web searches and extracts key facts.
    
    This agent:
    1. Takes the user query from state
    2. Performs web search using Tavily
    3. Extracts and structures key information
    4. Updates state with gathered facts
    5. Sets next_agent to return control to supervisor
    
    Args:
        state: Current workflow state containing user_query
        
    Returns:
        Updated state with gathered_facts populated
    """
    print("\n🔍 Research Agent: Starting research...")
    
    user_query = state["user_query"]
    iteration = state.get("iteration", 0) + 1
    
    try:
        # Initialize Tavily search tool
        search = TavilySearchResults(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=False
        )
        
        # Perform the search
        print(f"🔍 Research Agent: Searching for: '{user_query}'")
        search_results = search.invoke({"query": user_query})
        
        # Extract and structure the facts
        gathered_facts = []
        
        # Add the direct answer if available
        if search_results and len(search_results) > 0:
            for idx, result in enumerate(search_results, 1):
                if isinstance(result, dict):
                    content = result.get("content", "")
                    url = result.get("url", "")
                    if content:
                        fact = f"Source {idx}: {content}"
                        if url:
                            fact += f" (URL: {url})"
                        gathered_facts.append(fact)
        
        # Use LLM to synthesize and extract key facts from search results
        if gathered_facts:
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.3,
                api_key=os.getenv("OPENAI_API_KEY")
            )
            
            synthesis_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a research assistant. Extract and list the most important facts from the search results. Be concise and factual. List 3-5 key facts."),
                ("user", "Search query: {query}\n\nSearch results:\n{results}\n\nExtract key facts:")
            ])
            
            chain = synthesis_prompt | llm
            response = chain.invoke({
                "query": user_query,
                "results": "\n\n".join(gathered_facts)
            })
            
            # Parse the synthesized facts
            synthesized_text = response.content
            synthesized_facts = [
                fact.strip() 
                for fact in synthesized_text.split("\n") 
                if fact.strip() and not fact.strip().startswith("#")
            ]
            
            print(f"🔍 Research Agent: Found {len(synthesized_facts)} key facts")
            
            return {
                **state,
                "gathered_facts": synthesized_facts if synthesized_facts else gathered_facts,
                "next_agent": "supervisor",
                "iteration": iteration,
                "messages": state.get("messages", []) + [
                    {"role": "assistant", "content": f"Research completed. Found {len(synthesized_facts)} key facts."}
                ]
            }
        else:
            print("🔍 Research Agent: No results found")
            return {
                **state,
                "gathered_facts": ["No relevant information found for this query."],
                "next_agent": "supervisor",
                "iteration": iteration,
                "messages": state.get("messages", []) + [
                    {"role": "assistant", "content": "Research completed but no relevant results found."}
                ]
            }
            
    except Exception as e:
        print(f"⚠️ Research Agent: Error during research: {str(e)}")
        return {
            **state,
            "gathered_facts": [f"Research error: {str(e)}"],
            "next_agent": "supervisor",
            "iteration": iteration,
            "messages": state.get("messages", []) + [
                {"role": "assistant", "content": f"Research encountered an error: {str(e)}"}
            ]
        }

