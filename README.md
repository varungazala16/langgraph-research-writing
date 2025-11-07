# LangGraph Multi-Agent Research & Writing System

A sophisticated multi-agent system built with LangGraph that orchestrates research and writing tasks using a supervisor pattern. The system uses specialized agents for distinct tasks, managed by a supervisor that intelligently routes requests based on context.

## Architecture

The system consists of three main agents:

- **Supervisor Agent**: Analyzes user queries and routes tasks to appropriate agents
- **Research Agent**: Performs web searches and gathers information using LangChain's search tools
- **Writing Agent**: Synthesizes research findings into coherent written content

### Workflow

```
User Query → Supervisor → Research Agent → Supervisor → Writing Agent → Final Output
                ↓                           ↑
            (routing)                  (hand-off)
```

## Features

- ✅ Stateful workflow with persistent context across agent transitions
- ✅ Intelligent task routing using LLM-based supervisor
- ✅ Real web search integration via Tavily
- ✅ Memory and context preservation across workflow steps
- ✅ Command-line interface for easy interaction
- ✅ Graceful hand-offs between agents

## Setup

### Prerequisites

- Python 3.9+
- OpenAI API key
- Tavily API key (for web search)

### Installation

1. Clone or download this repository:

```bash
cd scrollmark_langraph
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env.template .env
# Edit .env and add your API keys
```

### Getting API Keys

- **OpenAI**: Get your API key at https://platform.openai.com/api-keys
- **Tavily**: Sign up and get your API key at https://tavily.com

## Usage

### Command Line Interface

Run the system with a query:

```bash
python -m src.main "What are the latest developments in quantum computing?"
```

### Example Queries

```bash
# Pure research query
python -m src.main "What are the recent breakthroughs in fusion energy?"

# Writing task with research
python -m src.main "Research AI safety concerns and write a brief report"

# Direct writing request
python -m src.main "Write a summary about the impacts of climate change"
```

### Programmatic Usage

```python
from src.workflow import create_workflow
from src.state import AgentState

# Initialize workflow
workflow = create_workflow()

# Run with a query
initial_state = {
    "user_query": "Research quantum computing and write a summary",
    "gathered_facts": [],
    "draft_text": "",
    "messages": [],
    "iteration": 0
}

result = workflow.invoke(initial_state)
print(result["draft_text"])
```

## Project Structure

```
scrollmark_langraph/
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .env.example              # Environment variables template
├── src/
│   ├── __init__.py
│   ├── state.py              # Shared state model
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── research_agent.py # Research agent implementation
│   │   ├── writing_agent.py  # Writing agent implementation
│   │   └── supervisor.py     # Supervisor agent implementation
│   ├── workflow.py           # LangGraph workflow definition
│   └── main.py               # CLI entry point
└── examples/
    └── example_queries.py    # Example usage demonstrations
```

## How It Works

### 1. State Management

The system uses a shared state object that persists across all agent transitions:

- `user_query`: Original user request
- `task_type`: Current task classification (research/writing)
- `gathered_facts`: Research findings collected by the research agent
- `draft_text`: Final written output from the writing agent
- `next_agent`: Routing decision made by supervisor
- `messages`: Conversation history
- `iteration`: Workflow step counter

### 2. Agent Flow

**Supervisor Agent**:
- Receives user query and current state
- Uses LLM to determine if research or writing is needed
- Routes to appropriate agent based on context

**Research Agent**:
- Performs web searches using Tavily
- Extracts and structures key information
- Updates state with gathered facts
- Returns control to supervisor

**Writing Agent**:
- Takes research findings from state
- Generates coherent written content
- Updates state with draft text
- Signals workflow completion

### 3. Conditional Routing

The workflow uses LangGraph's conditional edges to enable dynamic routing:
- Supervisor evaluates state and decides next step
- Research completes before writing begins
- System ensures logical task progression

## Customization

### Adding New Agents

1. Create a new agent file in `src/agents/`
2. Implement agent function with signature: `agent_node(state: AgentState) -> AgentState`
3. Add the agent as a node in `src/workflow.py`
4. Update supervisor routing logic to include new agent

### Modifying Search Tools

The research agent can be configured to use different search backends:
- Tavily (default)
- SerpAPI
- DuckDuckGo
- Custom search implementations

Edit `src/agents/research_agent.py` to swap search tools.

## Troubleshooting

**Import Errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**API Key Issues**: Verify your `.env` file has valid API keys

**Search Failures**: Check Tavily API key and internet connection

**LLM Errors**: Verify OpenAI API key and account has available credits

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

