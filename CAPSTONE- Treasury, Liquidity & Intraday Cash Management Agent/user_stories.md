# User Stories — Treasury, Liquidity & Intraday Cash Management Agent

18 stories total: 13 Functional, 5 Non-Functional. Covers all 6 PRD core
capabilities, including the bonus stress-scenario feature.

Assumed Agent Roster (from Specifications Document):
- **Cash & Position Aggregator Agent** — ingests/normalizes mock cash, nostro,
  funding gap, collateral, settlement, and market liquidity data
- **Forecasting Agent** — JSON-mode structured forecast of shortfalls
  (goal_task_list.py-style planner pattern)
- **Funding Recommendation Agent** — ReAct-style tool-calling agent that
  proposes funding actions
- **Alerting Agent** — threshold-breach detection and escalation
- **Commentary Agent** — guardrailed governance narrative generation
- **Stress Scenario Agent (Bonus)** — perturbs mock data to simulate shocks
- **Orchestrator** — Planner-Executor-Synthesizer pipeline coordinating all
  of the above

---

## Functional User Stories

### US-01: Aggregate intraday cash positions
- **Type:** Functional
- **Persona:** Treasury Analyst
- **Story:** As a Treasury Analyst, I want to see all intraday cash positions aggregated in one view, so that I don't have to check multiple systems manually.
- **Maps to PRD feature:** Cash/nostro/collateral/settlement/market monitoring
- **Maps to SDD agent(s):** Cash & Position Aggregator Agent
- **Priority:** Must Have
- **Notes:** Reads from mock_data.py time-series generator.

### US-02: Aggregate nostro balances across currencies
- **Type:** Functional
- **Persona:** Treasury Analyst
- **Story:** As a Treasury Analyst, I want nostro account balances aggregated across currencies, so that I can spot funding shortfalls by currency at a glance.
- **Maps to PRD feature:** Cash/nostro/collateral/settlement/market monitoring
- **Maps to SDD agent(s):** Cash & Position Aggregator Agent
- **Priority:** Must Have
- **Notes:** Output as structured JSON keyed by currency.

### US-03: Track funding gaps in real time
- **Type:** Functional
- **Persona:** Treasury Analyst
- **Story:** As a Treasury Analyst, I want funding gaps tracked as they emerge intraday, so that I can react before end-of-day settlement.
- **Maps to PRD feature:** Cash/nostro/collateral/settlement/market monitoring
- **Maps to SDD agent(s):** Cash & Position Aggregator Agent
- **Priority:** Must Have
- **Notes:** Gap = obligations due minus available liquidity.

### US-04: Monitor collateral movements
- **Type:** Functional
- **Persona:** Treasury Analyst
- **Story:** As a Treasury Analyst, I want to monitor incoming/outgoing collateral movements, so that I understand their effect on available liquidity.
- **Maps to PRD feature:** Cash/nostro/collateral/settlement/market monitoring
- **Maps to SDD agent(s):** Cash & Position Aggregator Agent
- **Priority:** Should Have
- **Notes:** Feeds directly into Forecasting Agent inputs.

### US-05: Track settlement obligations timeline
- **Type:** Functional
- **Persona:** Treasury Analyst
- **Story:** As a Treasury Analyst, I want a timeline of upcoming settlement obligations, so that I can sequence funding actions correctly.
- **Maps to PRD feature:** Cash/nostro/collateral/settlement/market monitoring
- **Maps to SDD agent(s):** Cash & Position Aggregator Agent
- **Priority:** Must Have
- **Notes:** Sorted ascending by obligation due-time.

### US-06: View market liquidity indicators
- **Type:** Functional
- **Persona:** Treasury Manager
- **Story:** As a Treasury Manager, I want to see current market liquidity indicators alongside internal positions, so that I can judge whether external conditions are worsening my risk.
- **Maps to PRD feature:** Cash/nostro/collateral/settlement/market monitoring
- **Maps to SDD agent(s):** Cash & Position Aggregator Agent
- **Priority:** Should Have
- **Notes:** Mock indicator feed, e.g. simulated repo rate/spread.

### US-07: Forecast intraday liquidity shortfall
- **Type:** Functional
- **Persona:** Treasury Manager
- **Story:** As a Treasury Manager, I want the system to forecast an upcoming liquidity shortfall before it happens, so that my team has lead time to act.
- **Maps to PRD feature:** Liquidity shortfall forecasting
- **Maps to SDD agent(s):** Forecasting Agent
- **Priority:** Must Have
- **Notes:** Uses response_format={"type":"json_object"}, same pattern as goal_task_list.py's planner().

### US-08: Receive funding action recommendations
- **Type:** Functional
- **Persona:** Treasury Manager
- **Story:** As a Treasury Manager, I want specific funding action recommendations when a shortfall is forecast, so that I can close the gap quickly.
- **Maps to PRD feature:** Funding action recommendation
- **Maps to SDD agent(s):** Funding Recommendation Agent
- **Priority:** Must Have
- **Notes:** ReAct-style: reasons over forecast + available funding sources before recommending.

### US-09: Get alerted on threshold breach
- **Type:** Functional
- **Persona:** Treasury Analyst
- **Story:** As a Treasury Analyst, I want to be alerted the moment a configured liquidity threshold is breached, so that I don't have to keep watching dashboards manually.
- **Maps to PRD feature:** Threshold-based alerting
- **Maps to SDD agent(s):** Alerting Agent
- **Priority:** Must Have
- **Notes:** Escalation severity levels defined in SDD section 6.

### US-10: Configure liquidity thresholds per account/currency
- **Type:** Functional
- **Persona:** Treasury Manager
- **Story:** As a Treasury Manager, I want to configure thresholds per account and currency, so that alerts reflect our actual risk appetite rather than a single global limit.
- **Maps to PRD feature:** Threshold-based alerting
- **Maps to SDD agent(s):** Alerting Agent
- **Priority:** Should Have
- **Notes:** Config object read by Alerting Agent at runtime.

### US-11: Generate daily governance commentary
- **Type:** Functional
- **Persona:** CFO Viewer
- **Story:** As a CFO, I want a clear written liquidity commentary generated for the daily governance call, so that I can brief stakeholders without compiling it myself.
- **Maps to PRD feature:** Governance-ready narrative generation
- **Maps to SDD agent(s):** Commentary Agent
- **Priority:** Must Have
- **Notes:** Must pass through Guardrails before being shown.

### US-12 (Bonus): Simulate delayed settlement stress scenario
- **Type:** Functional
- **Persona:** Treasury Manager
- **Story:** As a Treasury Manager, I want to simulate a delayed settlement scenario, so that I can see its projected impact on liquidity before it happens for real.
- **Maps to PRD feature:** Stress scenario simulation (bonus)
- **Maps to SDD agent(s):** Stress Scenario Agent
- **Priority:** Could Have
- **Notes:** Perturbs mock settlement obligation data, re-runs Forecasting Agent.

### US-13 (Bonus): Simulate large client withdrawal stress scenario
- **Type:** Functional
- **Persona:** Treasury Manager
- **Story:** As a Treasury Manager, I want to simulate a large, unexpected client withdrawal, so that I can stress-test our funding buffer.
- **Maps to PRD feature:** Stress scenario simulation (bonus)
- **Maps to SDD agent(s):** Stress Scenario Agent
- **Priority:** Could Have
- **Notes:** Perturbs mock cash position data, re-runs Forecasting + Alerting Agents.

---

## Non-Functional User Stories

### US-14: Structured outputs are always valid JSON
- **Type:** Non-Functional
- **Persona:** Engineering/QA
- **Story:** As an engineer, I want every LLM call in the system to return valid JSON matching its defined schema, so that downstream agents never fail on malformed input.
- **Maps to PRD feature:** (cross-cutting — all)
- **Maps to SDD agent(s):** All LLM-calling agents
- **Priority:** Must Have
- **Notes:** Validated in eval_harness.py.

### US-15: Alerts fire within 5 seconds of a breach
- **Type:** Non-Functional
- **Persona:** Treasury Analyst
- **Story:** As a Treasury Analyst, I want threshold-breach alerts to fire within 5 seconds of the breach appearing in the data stream, so that alerts stay useful for intraday decisions.
- **Maps to PRD feature:** Threshold-based alerting
- **Maps to SDD agent(s):** Alerting Agent
- **Priority:** Must Have
- **Notes:** Measurable against synthetic timestamped mock data.

### US-16: Guardrails prevent fabricated figures in commentary
- **Type:** Non-Functional
- **Persona:** CFO Viewer
- **Story:** As a CFO, I want the generated commentary to never state a number that isn't traceable to actual source data, so that I can trust it in front of stakeholders.
- **Maps to PRD feature:** Governance-ready narrative generation
- **Maps to SDD agent(s):** Commentary Agent, Guardrails module
- **Priority:** Must Have
- **Notes:** Guardrail check runs post-generation, pre-display.

### US-17: Agent decisions are logged for audit
- **Type:** Non-Functional
- **Persona:** Compliance/QA
- **Story:** As a compliance reviewer, I want every agent decision (forecast, recommendation, alert, commentary) logged with its inputs, so that today's run can be reconstructed after the fact.
- **Maps to PRD feature:** (cross-cutting — all)
- **Maps to SDD agent(s):** Orchestrator
- **Priority:** Should Have
- **Notes:** Simple structured log file is sufficient for demo scope.

### US-18: Full demo run completes within budget
- **Type:** Non-Functional
- **Persona:** Engineering
- **Story:** As the project owner, I want a full end-to-end run (aggregation → forecast → recommendation → alert → commentary) to complete within a short, predictable time and cost, so that it's viable to demo live to a client.
- **Maps to PRD feature:** (cross-cutting — delivery constraint)
- **Maps to SDD agent(s):** Orchestrator
- **Priority:** Must Have
- **Notes:** Use gpt-4o-mini throughout to keep latency/cost low for the demo.

---

## Coverage Summary

| ID | Type | Priority | PRD Feature |
|----|------|----------|--------------|
| US-01 | Functional | Must | Monitoring |
| US-02 | Functional | Must | Monitoring |
| US-03 | Functional | Must | Monitoring |
| US-04 | Functional | Should | Monitoring |
| US-05 | Functional | Must | Monitoring |
| US-06 | Functional | Should | Monitoring |
| US-07 | Functional | Must | Forecasting |
| US-08 | Functional | Must | Funding recommendation |
| US-09 | Functional | Must | Threshold alerting |
| US-10 | Functional | Should | Threshold alerting |
| US-11 | Functional | Must | Governance commentary |
| US-12 | Functional | Could | Stress simulation (bonus) |
| US-13 | Functional | Could | Stress simulation (bonus) |
| US-14 | Non-Functional | Must | Cross-cutting |
| US-15 | Non-Functional | Must | Threshold alerting |
| US-16 | Non-Functional | Must | Governance commentary |
| US-17 | Non-Functional | Should | Cross-cutting |
| US-18 | Non-Functional | Must | Cross-cutting |