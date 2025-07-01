# WiseStreet Agent Workflows Overview

We are defining multiple distinct agent workflows ("strategies") that reuse our core sub-agent infrastructure (macro, sentiment, earnings, valuation, news, etc.) but vary in:

- Objective  
- Control logic / orchestration  
- Type of output

These workflows act as "templates" for different user goals. Each one can be thought of as a different "persona" or strategy powered by the same agent team.

---

## Common Sub-Agents (Shared by All Workflows)

| Agent               | Role                                                                 |
|---------------------|----------------------------------------------------------------------|
| MacroAgent          | Understand global events, GDP, inflation, rates, central bank moves |
| NewsAgent           | Aggregate & summarize recent news from APIs                         |
| SentimentAgent      | Pull sentiment from Reddit, Twitter, YouTube                        |
| EarningsAgent       | Analyze recent earnings reports (revenue, EPS, etc.)                |
| ValuationAgent      | Estimate valuation using models (DCF, P/E, peer comps)              |
| BalanceSheetAgent   | Analyze company assets, liabilities, liquidity, solvency            |
| CashflowAgent       | Examine free cash flow, operating cash flow, CapEx                  |
| RatioAgent          | Pull profitability ratios like ROE, ROIC, margins                   |
| TranscriptAgent     | Summarize earnings calls for tone, outlook, and red/green flags     |
| RiskAgent           | Flag risks: legal, debt, financial health, market exposure          |
| TechnicalAgent      | Surface technical trends like RSI, MACD, moving averages            |
| SectorTrendsAgent   | Identify hot sectors based on macro, capital flows, earnings        |

---

## Workflow 1: Retail Research Assistant (Default Setup)

### Goal:
Answer user queries about companies, sectors, or macro themes with relevant insights.

### Flow:
1. User asks a question: *"What’s happening with Tesla?"*
2. Head Agent identifies topic scope (Company)
3. Routes query to:
   - NewsAgent
   - SentimentAgent
   - EarningsAgent
   - ValuationAgent
   - RiskAgent
4. Collects all data and summarizes in TL;DR for user

### Output:
- Clear cards per agent
- Final summary with insight and recommendation

---

## Workflow 2: Trade Idea Generator

### Goal:
Automatically scan macro trends, sectors, and company fundamentals to propose high-conviction investment ideas.

### Flow:
1. Head Agent triggers:
   - MacroAgent + NewsAgent → Understand current economic conditions
2. Interprets market environment:
   - Bullish, Bearish, Neutral, Volatile, etc.
3. Based on view → scans promising sectors:
   - SectorTrendsAgent → picks active industries
4. Within sectors:
   - EarningsAgent → High-growth, improving fundamentals
   - BalanceSheetAgent + CashflowAgent + RatioAgent → Financial strength
   - ValuationAgent → Undervaluation screening
5. Final filtering:
   - SentimentAgent → Public mood
   - TranscriptAgent → Red/green flags
   - RiskAgent → Remove risky bets

### Output:
- Trade idea name
- Thesis: Why now?
- Risks, metrics, data cards
- Confidence level: High / Medium / Speculative

---

## Ideas for Other Workflows

### Portfolio Analyzer

#### Input:
- CSV or JSON of user holdings

#### Flow:
For each stock:
- NewsAgent
- EarningsAgent
- ValuationAgent
- RiskAgent
- BalanceSheetAgent
- CashflowAgent

Then:
- Flag underperformance, risks
- Suggest rebalancing

---

### Explain Like I’m 15

#### Flow:
- Any financial topic entered
- All agent output is summarized in ultra-simple English

---

### Deep Dive Mode

#### Example Prompt:
*"Full breakdown of Adani Enterprises"*

#### Response Structure:
1. Macro Fit  
2. Sector Dynamics  
3. Fundamentals (Earnings, Ratios, Balance Sheet, Cashflow)  
4. Sentiment  
5. Valuation  
6. Risk Map  
7. Transcript Summary  
8. Bull vs Bear Case

---

