# WiseStreet MDT — Local Agent-Based Terminal App (PRD)

## Objective

Build a terminal-based, agentic prototype of WiseStreet using OpenAI's Function Calling + Manager Pattern architecture.

The goal is to simulate a real AI-powered financial research desk, where:
- The **Head Agent** understands the user's full query, determines the needed sub-tasks.
- It delegates each sub-task to a domain-specialized **Sub-Agent** using structured tool calling.
- Each sub-agent returns structured data or summary based on natural-language instructions, not just fixed parameters.
- The Head Agent synthesizes a clear final summary with structured insights.

---

## Architecture Overview

### 👨‍🏫 Head Agent (Manager)
- Model: GPT-4o
- Role: Fully interprets user query, breaks it into subtasks
- Uses OpenAI tool-calling to dispatch instructions
- Synthesizes the returned agent responses
- Output: Final summary (TL;DR), plus optional cards from each agent

---

## 🧠 Sub-Agent Specifications (Tool Functions)

Each sub-agent is a **GPT-invoked tool** that receives detailed prompts and executes a domain-specific task. These tools are not just API wrappers — they simulate experts that interpret instructions and return meaningful intelligence.

### 1. `get_news(prompt: str)`
- Purpose: Gathers and summarizes latest relevant news about any topic
- Accepts full open-ended natural language instructions
- Output: Bullet point summary with optional sources
- Examples:
  - "Summarize news from the last 5 days about US-China tech trade restrictions"
  - "Get recent news on crude oil supply disruptions globally"

### 2. `get_sentiment(prompt: str)`
- Purpose: Assesses public sentiment from social platforms (Reddit, YouTube, etc.)
- Works for companies, commodities, events, or any theme
- Examples:
  - "What’s the retail sentiment around Tesla after their earnings?"
  - "How are Indian investors reacting to rising gold prices?"

### 3. `get_earnings(prompt: str)`
- Purpose: Returns interpreted earnings performance of a company
- Includes revenue, EPS, YoY growth, management commentary
- Examples:
  - "What are the key highlights from HDFC Bank’s last earnings report?"

### 4. `get_macro(prompt: str)`
- Purpose: Provides macroeconomic insights or event context
- Works for global, country-level, or industry-wide economic questions
- Examples:
  - "Explain how inflation is affecting FMCG companies in India"
  - "Summarize the impact of rising interest rates on the real estate sector"

### 5. `get_valuation(prompt: str)`
- Purpose: Explains a company’s valuation logic, compares peers, or estimates fair price
- Returns metrics like P/E, DCF range, multiples
- Examples:
  - "Compare valuation between Infosys and TCS"
  - "What is a reasonable price range for Zomato stock?"

---

## Folder Structure

wisestreet_mdt/
├── main.py
├── agents/
│ ├── head_agent.py # Head Agent logic with tool calling
│ ├── tools.py # Tool function definitions
│ └── utils.py # Optional helpers
├── data/ # Mock responses or static JSONs
├── .env # API key
├── requirements.txt
└── references/
└── wisestreet_agent_prd.md


---

## Development Plan

- Start with terminal input/output (no UI or backend yet)
- Implement only `get_news(prompt)` first with fake or static data
- Use OpenAI's `tool_call` style to simulate manager-agent architecture
- Test flow: user query → head agent → tool call → mock output → summary

---

## Final Objective

Prove the intelligent interaction between a head agent and multiple thinking sub-agents, using prompt engineering and GPT-based orchestration. This prototype forms the foundation for a future real-time investing research app.

---
