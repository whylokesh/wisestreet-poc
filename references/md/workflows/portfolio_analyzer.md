# Portfolio Analyzer

## Objective

Analyze and evaluate a user's current investment portfolio using AI agents. Identify strengths, weaknesses, risk exposure, and suggest intelligent rebalancing and improvements.

Our goal is to give every investor an intelligent research analyst who can:
- Audit portfolio fundamentals and diversification
- Flag red flags and imbalances
- Recommend improvements based on goals and risk
- Educate the user as they go

This is a personalized, one-click portfolio insight engine — not a general chatbot.

---

## How Users Interact

1. User connects portfolio (via broker integration or CSV upload)
2. Agent extracts holdings, weights, and historical trades
3. AI sub-agents analyze each stock
4. Head Agent compiles a clean, understandable insight report
5. User can ask follow-ups like:
   - “What’s the weakest stock here?”
   - “Where am I overexposed?”
   - “Should I trim X or add more Y?”

---

## Sub-Agent Orchestration Logic

### Flow:

1. Portfolio data (tickers, weights, buy prices) is received
2. Head Agent calls the following:

- **EarningsAgent** + **ValuationAgent**: Analyze fundamentals
- **SentimentAgent** + **TranscriptAgent**: Market emotion + management tone
- **RiskAgent**: Flag red flags (volatility, debt, legal)
- **BalanceSheetAgent** + **CashflowAgent**: Financial stability
- **DiversificationAgent**: Sector/style/region exposure
- **GoalFitAgent**: Goal alignment
- **BehavioralAgent**: Bad investing patterns
- **ScenarioAgent**: Simulate what-if conditions

3. Head Agent synthesizes everything and returns:
   - A summary report
   - Highlights (good & bad)
   - Suggested actions

---

## Agent Breakdown

| Agent               | Purpose                                                  |
|--------------------|----------------------------------------------------------|
| EarningsAgent       | Evaluates earnings quality and momentum                 |
| ValuationAgent      | Determines if stock is under/overvalued                 |
| SentimentAgent      | Understands market sentiment                            |
| TranscriptAgent     | Analyzes management tone in earnings calls              |
| RiskAgent           | Flags risk (debt, legal, volatility)                    |
| BalanceSheetAgent   | Reviews assets, liabilities, solvency                   |
| CashflowAgent       | Checks free cash flow and operating cash                |
| DiversificationAgent| Checks exposure across sectors, styles, and geography  |
| GoalFitAgent        | Matches portfolio with user's stated financial goals    |
| BehavioralAgent     | Identifies emotional investing patterns                 |
| ScenarioAgent       | Simulates “what-if” market conditions                   |

---

## Output Schema (Sample)

```json
{
  "summary": "Your portfolio is solid in earnings growth, but exposed to mid-cap tech volatility. Consider trimming 2 names.",
  "overexposure": ["Tech (56%)"],
  "high_risk": ["StockA (low FCF)", "StockB (high debt)"]
}
```

## Visual Design Philosophy

- Dashboard-style layout  
- Portfolio pie chart, sector bars, and regional maps  
- Risky holdings in red, strong ones in green  
- Action cards: **Trim**, **Hold**, **Double Down**, **Exit**, **Replace**  
- Chat window for follow-up questions  

---

## Example Use Cases

- “I uploaded my Groww portfolio and it told me to exit 1 stock, trim 2, double down on 1.”  
- “My risk score is higher than average. How can I reduce it?”  
- “I’m overweight Tech and missed opportunities in Healthcare.”  

---

## Future Enhancements

- Connect with Zerodha, Groww, or Smallcase for live sync  
- Show historical alpha vs benchmarks  
- Suggest ETFs to improve diversification  
- Add disclaimers and advisor-grade risk profiling  
- Create AI scoring system per holding  
- Monthly email or report updates  

---

## Power Features (Planned)

| Feature               | Description                                                             |
|-----------------------|-------------------------------------------------------------------------|
| Behavioral Analysis    | Detect emotional mistakes like panic selling, FOMO, or overtrading      |
| Goal-Based Matching    | See which assets support your goals — and which don’t                  |
| What-If Simulator      | “What if I move 20% into Pharma?” or “What if interest rates go up?”   |
| Peer Comparison        | See how your portfolio stacks up vs. peers or model investors           |
| Narrative Generator    | "Why do I own this stock?" explained in simple, natural language        |
