# Agentic Stock Screener Workflow

## Overview

The **Agentic Stock Screener** is a next-generation AI-powered screener that replaces traditional filter-based screening with an intelligent, goal-driven analysis engine. 

Users provide a natural language query, and WiseStreet's team of AI agents collaboratively interprets the intent, applies relevant screening logic, and surfaces a ranked, explainable list of investment opportunities.

---

## What Makes This Different

Traditional stock screeners let users apply rigid filters like:

- P/E < 20  
- Market Cap > 10B  
- Dividend Yield > 3%

**Agentic Screeners** allow users to ask:

> “Find undervalued Indian EV companies with high sentiment and strong recent earnings.”

The system interprets that goal and determines:

- What “undervalued” means in context (e.g., P/E, DCF)
- What data points are relevant (sentiment, earnings, etc.)
- Which stocks qualify and why

---

## Target Users

- Retail investors who want ideas without deep filter knowledge  
- Professional analysts who want fast idea generation  
- Financial educators and advisors  

---

## Workflow Breakdown

### 1. User Query (Intent)

Users enter a high-level prompt:

- “Safe mid-cap stocks in healthcare”
- “Green energy stocks with strong Q1”
- “Small-cap IT stocks trending on Reddit”

---

### 2. Head Screener Agent

- Parses user intent into components  
- Delegates to relevant sub-agents:  
  - **Fundamental Agent**  
  - **Earnings Agent**  
  - **Sentiment Agent**  
  - **Macro Agent** (optional)  
  - **Risk Agent** (optional)  

---

### 3. Sub-Agent Actions

**Fundamental Agent**

- Filters by P/E, EPS growth, ROE, etc.

**Earnings Agent**

- Checks last 2 quarters of earnings  
- Extracts surprise beats, revenue trends  

**Sentiment Agent**

- Pulls recent Reddit, Twitter, YouTube mentions  
- Scores community optimism  

**Macro Agent**

- Screens sectors aligned with current trends (e.g., budget, rate cuts)

**Risk Agent (future)**

- Flags debt, litigation, beta, or management issues  

---

### 4. Scoring & Ranking

Each stock gets a **composite score** based on:

- Quantitative metrics  
- Agent confidence  
- Sentiment and macro alignment  

---

### 5. Output

A ranked list of 3–10 stocks.  
For each:

- Score  
- TL;DR summary  
- Agent comments (why it was picked)  
- Source links  

**Display Formats**:

- Interactive Table View  
- Card View  
- PDF Export  

---

## Example Query & Output

**Input:**

> “Find undervalued large-cap stocks in India with recent bullish sentiment.”

**Output Table:**

| Ticker     | Name               | Score | Summary                                                  |
|------------|--------------------|-------|-----------------------------------------------------------|
| TCS        | Tata Consultancy   | 9.1   | Undervalued vs peers, bullish Reddit threads, steady EPS |
| INFY       | Infosys            | 8.9   | Recent earnings beat, macro tailwinds, social optimism   |
| HDFCBANK   | HDFC Bank          | 8.7   | Consistent ROE, P/E below avg, strong analyst coverage   |

---

## Key Advantages

- No filter knowledge required  
- Conversational and adaptive  
- Fully explainable  
- Integrates all WiseStreet sub-agents  

---

## Future Ideas

- Save screeners as “watchlists”  
- Alerting on screener triggers  
- Screeners by investor type (e.g., conservative, growth)  
- Sector templates (e.g., AI stocks, Pharma, Fintech)  
- Multi-agent debates (“Which of these is best?” logic)

---

## MVP Plan

- Input: Text box with prompt  
- Output: Table of 3–5 ideas  
- Agents: Head Screener + Fundamentals + Sentiment + Earnings  
- Deployment: Host on local terminal first → Next.js frontend later

---

## Summary

The **Agentic Stock Screener** turns vague investment goals into high-quality, research-backed stock ideas.

It mimics how a smart analyst team works — breaking goals into steps, analyzing data from multiple angles, and justifying every pick.

> It’s not a tool — it’s a decision-making assistant for modern investors.
