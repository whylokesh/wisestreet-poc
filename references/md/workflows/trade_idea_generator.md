# Trade Idea Generator Workflow

## Objective

Automatically generate and publish a curated set of high-conviction trade ideas based on real-time macroeconomic conditions, sector trends, and company fundamentals.

This is not a conversational interface. Instead, it operates like an e-commerce-style discovery platform, where users browse trade ideas in a catalog-like interface. Each trade idea is a fully analyzed, research-backed product with a summary, metrics, and source links.

**Users can:**
- Browse a feed of trade ideas based on market conditions
- Filter by sector, region, risk profile, or strategy (value/growth)
- Click into any idea to see full breakdown, sources, and insights
- Follow-up or deep-dive on ideas using our Q&A agents

## Sub-Agent Orchestration Logic

### Flow:

1. Head Agent runs scheduled or manual idea generation (daily/weekly)

2. **Phase 1: Market Scan**
   - MacroAgent + NewsAgent assess the current economic climate
   - Determine if outlook is bullish, bearish, volatile, or sector-specific

3. **Phase 2: Sector & Theme Discovery**
   - SectorTrendsAgent recommends sectors/themes with upside

4. **Phase 3: Idea Mining per Sector**
   - For top sectors:
     - EarningsAgent, ValuationAgent, RatioAgent, BalanceSheetAgent, CashflowAgent pull key financials
     - SentimentAgent, TranscriptAgent, RiskAgent validate narrative and flag concerns

5. **Phase 4: Trade Idea Curation**
   - Head Agent ranks, scores, and packages ideas into readable profiles
   - Output → Pushed to UI for browsing

## Agent Breakdown

| Agent | Purpose |
|-------|---------|
| MacroAgent | Defines market backdrop |
| NewsAgent | Captures current events and catalysts |
| SectorTrendsAgent | Finds which sectors are gaining capital, media attention, or growth |
| EarningsAgent | Surfaces companies with strong recent earnings |
| ValuationAgent | Filters undervalued stocks or those near price targets |
| RatioAgent | Adds profitability filters (ROE, margin, etc.) |
| BalanceSheetAgent | Evaluates solvency and debt load |
| CashflowAgent | Looks for positive cashflow, FCF, and CapEx efficiency |
| TranscriptAgent | Looks for optimism or risk in recent management communication |
| RiskAgent | Flags any deal-breakers or vulnerabilities |
| SentimentAgent | Measures social confidence & hype |

## Output Schema

```json
{
  "macro_outlook": "bullish",
  "sectors": ["Green Energy", "Defense", "Fintech"],
  "ideas": [
    {
      "name": "StockName",
      "sector": "Green Energy",
      "summary": "This company has rising earnings, is undervalued vs peers, and has strong positive sentiment.",
      "metrics": {
        "eps_growth": "22% YoY",
        "pe_ratio": 14.3,
        "roe": "18%",
        "debt_to_equity": 0.3
      },
      "sentiment": "bullish",
      "risk": "Low",
      "confidence": "High",
      "sources": ["AlphaVantage", "Reddit", "TradingEconomics"]
    }
  ]
}
```

## Visual Design Philosophy

- Card-based UI for each idea (like products on Amazon)
- Filter sidebar: Sector, Market Cap, Risk Level, Strategy Type
- Detail view per idea: summary, agent insights, citations, explore deeper with chat
- Call-to-action: Save to watchlist, run Q&A on this idea, share

## Example Use Cases

- User lands on homepage and sees 5 fresh trade ideas
- Filters to "Low Risk + Undervalued + Fintech"
- Clicks into "Company X" → reads agent cards, sentiment, risk summary
- Uses Chat to ask, "Why is its debt low compared to peers?"

## Future Enhancements

- Tag ideas by investment strategy: Value, Growth, Momentum, Dividend
- Follow sectors or themes (like tags)
- Add performance tracking (real returns over time)
- Integrate backtests, sentiment timelines, earnings season filters
- Premium tier: Early access to high confidence ideas