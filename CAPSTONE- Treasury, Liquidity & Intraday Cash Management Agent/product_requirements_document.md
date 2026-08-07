# Prompt: Generate Product Requirements Document (PRD)

Paste this into GitHub Copilot Chat (with your `CAPSTONE - Treasury, Liquidity & Intraday Cash Management Agent` folder open in VS Code so Copilot has workspace context).

---

```
You are a senior product manager specializing in agentic AI systems for financial
services. Generate a complete Product Requirements Document (PRD) in Markdown and
save it as `product_requirements_document.md`.

CONTEXT
Project name: Treasury, Liquidity & Intraday Cash Management Agent
Type: Agentic AI capstone project (final project of a multi-week Agentic AI course
covering tool-calling agents, ReAct, planner-executor-synthesizer pipelines,
multi-agent handoff, RAG, memory (short + long term), guardrails, and evaluation
harnesses — see /Agentic AI Projects folder for prior implementations to reuse as
architectural patterns).
Audience: Bank/corporate treasury teams who need intraday visibility into cash and
liquidity risk.
Delivery constraint: Must be demoable to a client in a couple of hours — favor a
tight, working vertical slice over broad coverage.

PROBLEM STATEMENT
Treasury teams manually aggregate cash positions, nostro balances, funding gaps,
collateral movements, and settlement obligations across systems, causing delayed
detection of intraday liquidity shortfalls and slow response to threshold breaches.

PRODUCT SCOPE
Build an agentic solution that:
1. Monitors intraday cash positions, nostro account balances, funding gaps,
   collateral movements, settlement obligations, and market liquidity indicators.
2. Forecasts liquidity shortfalls before they occur.
3. Recommends specific funding actions to close projected gaps.
4. Alerts treasury teams when configurable thresholds are breached.
5. Generates natural-language liquidity commentary for daily governance calls.
6. (Bonus / stretch) Simulates stress scenarios: delayed settlement, market
   volatility spikes, large client withdrawals — and reports impact on liquidity.

OBJECTIVE
Help treasury teams maintain liquidity discipline and respond faster to intraday
funding and settlement risk.

LEARNING TAKEAWAYS TO DEMONSTRATE (map each to a PRD feature/section)
Cash-position aggregation, liquidity forecasting, threshold-based alerting,
treasury workflow automation, scenario simulation, governance-ready narrative
generation.

INSTRUCTIONS — Structure the PRD with these sections:
1. Executive Summary (3-4 sentences)
2. Problem Statement & Business Context
3. Goals & Objectives (business goals vs. technical/learning goals — separate them)
4. Target Users / Personas (e.g., Treasury Analyst, Treasury Manager, CFO viewer)
5. Scope
   - In scope (numbered)
   - Out of scope (numbered, explicit — e.g., real trade execution, real bank
     integrations, real-money movement)
6. Core Capabilities / Feature List (numbered, each mapped to one of the 6 scope
   items above; note which are MVP vs. bonus/stretch)
7. Agentic Architecture Overview (high level only — name the agent roles, e.g.,
   Data-Aggregator Agent, Forecasting Agent, Alerting Agent, Commentary/Narrative
   Agent, Orchestrator — detailed design belongs in the specifications document,
   not here)
8. Data Inputs (list assumed data sources — mock/synthetic data is acceptable
   given the time constraint: intraday cash ledger, nostro balances, settlement
   queue, collateral positions, market liquidity feed)
9. Success Metrics (how you'll know the demo/project succeeded — both product
   metrics like "shortfall detected before breach" and technical metrics like
   "agent forecast accuracy on synthetic data")
10. Assumptions & Constraints (2-hour build window, synthetic/mock data, no live
    bank connectivity, single-session demo)
11. Risks & Mitigations
12. Deliverables Checklist (PRD, Specifications Doc, User Stories, Acceptance
    Criteria, Technical Prompts, Source Code, optional Demo HTML page, optional
    3-5 slide deck)
13. Open Questions

STYLE
- Concise, numbered, scannable — this will be read by both a course reviewer and
  a mock "client."
- No filler language. Every bullet should be specific enough to turn into a user
  story later.
- Do not write code or detailed technical design here — that belongs in the
  specifications document (next artifact in the sequence).
```

---

**Next in sequence (once PRD is approved):** Specifications Document → User
Stories (aim for 20, split functional/non-functional) → Acceptance Criteria →
Technical Prompts → Source Code.

Say "next" when you want the Specifications Document prompt.