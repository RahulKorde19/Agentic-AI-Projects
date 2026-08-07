### Slide 1 — Title & Problem
- Title: "Treasury, Liquidity & Intraday Cash Management Agent"
- Problem: Treasury teams need faster visibility into cash, settlement, and funding risk before small gaps become urgent issues.
- Presenter: Presenter Name / 2026-08-06

---

### Slide 2 — What It Does
- Monitors cash positions across sample accounts acct-001, acct-002, acct-003, and acct-004, with nostro totals of $3,900,000 USD / €1,800,000 EUR / £960,000 GBP — gives the desk a single view of available liquidity.
- Forecasts near-term liquidity pressure and identified a $500,000 USD projected shortfall about 120 minutes before the breach window.
- Recommends a funding action, and the live run selected an Intraday Credit Line for the $500,000 USD gap.
- Alerts on threshold breaches, including a funding_gap alert on acct-002 and a repo_rate_spread alert.
- Generates governance commentary, and the live run showed a safe fallback summary when the AI-written version could not be verified.
- Simulates stress scenarios, including a delayed settlement case that extended the breach window to 180 minutes.

---

### Slide 3 — How It Works (Architecture, Simplified)
- Data Aggregator → cash_position_agent combines balances, funding gaps, collateral movements, and settlement timing into one structured snapshot.
- Forecaster → forecasting_agent projects the liquidity shortfall for acct-001 and explains the $500,000 USD gap.
- Funding Advisor → funding_recommendation_agent recommends an Intraday Credit Line for the projected shortfall.
- Alert Watcher → alerting_agent raises 2 active alerts for the funding gap and repo-rate spread breach.
- Report Writer → commentary_agent turns the result into a governance-ready summary; when the wording fails the check, the system shows a safe template summary instead.
- Safety design → the system double-checks its own written summary before showing it, and this fallback behavior was exercised in the live run.

---

### Slide 4 — Live Demo / Sample Output
- Live run output showed shortfall_projected = true, amount = $500,000 USD, and estimated time to breach = 120 minutes on acct-001.
- Funding recommendation: Intraday Credit Line, recommended amount = $500,000 USD.
- Alerts active: 2 — funding_gap breach on acct-002 (threshold 100,000 vs actual 1,000,000) and repo_rate_spread breach (threshold 0.4 vs actual 0.55).
- Commentary shown: "Liquidity status: forecast shortfall=yes; active alerts=2." from the safe fallback because the AI-written commentary did not pass the check.
- Stress scenario: delayed_settlement with a 2-hour delay kept the shortfall at $500,000 USD but extended the breach window to 180 minutes.
- Note: all figures above are from synthetic/mock demo data, not live bank or market feeds.

---

### Slide 5 — Impact & Next Steps
- Speeds response to intraday funding and settlement risk by turning scattered signals into one decision-ready view.
- Makes risk testing visible so treasury teams can explore what-if scenarios before a shortfall becomes urgent.
- Next step: connect the demo to real bank and market data sources.
- Next step: expand the stress-scenario library beyond delayed settlement and repo-rate stress.
- Next step: tighten the commentary check so fewer runs fall back to the safe summary.

---

- Speaker note — Slide 1: 30 seconds
- Speaker note — Slide 2: 1 minute
- Speaker note — Slide 3: 1 minute
- Speaker note — Slide 4: 2 minutes
- Speaker note — Slide 5: 30 seconds
