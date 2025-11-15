# WiseStreet POC

**AI-powered, agentic financial research assistant for the terminal.**

## Overview

WiseStreet POC is a prototype that simulates a real financial research desk using OpenAI's function-calling and a manager/sub-agent architecture. The system is designed to:

- Interpret complex user queries about markets, companies, or macro trends.
- Break queries into subtasks and delegate to expert sub-agents.
- Aggregate and synthesize structured insights for the user.

## Features

- **Head Agent (Manager):**  
  Interprets user queries, orchestrates sub-agents, and synthesizes final answers.
- **Sub-Agents:**  
  - `get_news`: Summarizes latest relevant news.
  - `get_sentiment`: Assesses public sentiment from social platforms.
  - `get_earnings`: Interprets company earnings reports.
  - `get_macro`: Provides macroeconomic insights.
  - `get_valuation`: Explains company valuation and peer comparisons.
- **Extensible:**  
  Add new agents or data sources easily.
- **Local, terminal-based:**  
  No web UI or backend required.

## Architecture

```
User Query
   │
   ▼
Head Agent (Manager)
   │
   ├──> News Agent
   ├──> Sentiment Agent
   ├──> Earnings Agent
   ├──> Macro Agent
   └──> Valuation Agent
   │
   ▼
Synthesized Final Answer
```

## Setup

1. **Clone the repository**
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Set up your OpenAI API key:**
   - Create a `.env` file in the project root:
     ```
     OPENAI_API_KEY=your-key-here
     ```
4. *(Optional)* Add or configure mock/static data in the `data/` directory.

## Usage

> **Note:** The main entry point (`main.py`) is currently a placeholder. To test the agent logic, import and call the `head_agent` function from `agents/head_agent.py` in a Python shell or script.

Example usage:
```python
from openai import OpenAI
from agents.head_agent import head_agent

client = OpenAI()
query = "Summarize the latest news and sentiment about Apple after their earnings."
result = head_agent(query, client)
print(result)
```

## Development Plan

- Start with terminal input/output (no UI or backend).
- Implement and test each sub-agent with mock/static data.
- Expand to real APIs and more sophisticated orchestration.

## References

- [Product Requirements Document](references/wisestreet_agent_prd.md) 
