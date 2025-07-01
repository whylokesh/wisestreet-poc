# Retail Research Assistant Workflow

## Objective

Provide clear, actionable, and multi-dimensional insights on any financial query by acting as a smart co-pilot for retail investors.

This is the core Q&A interface — users ask anything, from stock-specific queries to macroeconomic questions.

## Sub-Agent Orchestration Logic

### Flow:

1. Head Agent receives user query → classifies intent (macro, company, sector, event, etc.)
2. Based on classification → routes task to the appropriate set of sub-agents
3. Sub-agents return structured outputs (summary, scores, charts, citations)
4. Head Agent synthesizes final response (TL;DR + expanded insight)

## Agent Breakdown

| Agent | Trigger Condition | Purpose |
|-------|------------------|---------|
| NewsAgent | Always | Provides recent, relevant news context |
| SentimentAgent | Always | Gauges social + community mood |
| EarningsAgent | On company queries | Pulls financial performance from earnings reports |
| ValuationAgent | On company queries | Gives valuation metrics and pricing view |
| MacroAgent | On macro / sector / country | Understands global indicators, monetary policy, trends |
| RiskAgent | On company or sector queries | Flags legal, structural, or market risks |

## Expected Output Schema

```json
{
  "summary": "TL;DR answer in plain English",
  "agent_cards": {
    "news": { "headlines": [], "summary": "..." },
    "sentiment": { "score": 0.7, "trend": "bullish" },
    "earnings": { "eps": "2.3", "revenue_growth": "15%" },
    "valuation": { "pe": 18.3, "target_price": 310 },
    "macro": { "trend": "disinflationary", "interest_rates": "stable" },
    "risk": { "score": 3.2, "notes": "..." }
  },
  "sources": ["newsapi.org", "reddit", "tradingeconomics"]
}
```

## Example Prompts

- "What's happening with Infosys lately?"
- "Why is the Indian auto sector rallying?"
- "What does the RBI rate hike mean for banks?"
- "Is HDFC Bank overvalued right now?"
- "Compare TCS vs Infosys from a valuation and earnings perspective"

## Future Enhancements

- Add plain-English explainers for any term (ROE, EPS, etc.)
- Integrate charts and heatmaps per agent card
- Save favorite stocks and watchlist-based auto reports
- Add voice input support
- Plugin for portfolio-level summaries