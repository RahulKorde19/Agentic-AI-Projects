# Technical Prompts — Treasury, Liquidity & Intraday Cash Management Agent

Paste each numbered block into Copilot Chat **in order** (later modules depend
on earlier ones). Each prompt is self-contained. Save the returned code as the
named file under `source_code/`.

Core structured-output pattern every LLM-calling module follows (from
`goal_task_list.py`):
```python
from openai import OpenAI
import json, os

client = OpenAI()  # reads OPENAI_API_KEY from environment

def call_llm(system_prompt, user_prompt):
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])
    return json.loads(r.choices[0].message.content)
```

---

## 1. mock_data.py
**Depends on:** none
**Implements:** foundation for AC-01–AC-06, AC-09, AC-12, AC-13

```
Write a Python module `mock_data.py` for a treasury liquidity demo system.

Purpose: generate realistic synthetic intraday data so the rest of the system
never needs a live bank connection.

Requirements:
- Functions: get_cash_positions(), get_nostro_balances(), get_funding_gaps(),
  get_collateral_movements(), get_settlement_obligations(),
  get_market_indicators() — each returns a list of dicts.
- Cash positions: account_id, currency, balance, timestamp (3-5 accounts,
  currencies mixed across USD/EUR/GBP).
- Nostro balances: account_id, currency, balance, correspondent_bank.
- Funding gaps: account_id, obligations_due, available_liquidity, timestamp.
- Collateral movements: movement_id, direction ("in"/"out"), amount,
  currency, settlement_time (some entries with settlement_time=None).
- Settlement obligations: obligation_id, account_id, amount, currency,
  due_time (ISO timestamps, spread across "today", some already in the past
  relative to a configurable `now()` to exercise the overdue case).
- Market indicators: indicator_name, value, threshold_reference, timestamp —
  include one indicator whose value exceeds its threshold_reference to allow
  a "stressed" condition to be testable.
- Include a `now()` helper returning a fixed, overridable "current" datetime
  so the whole system's timing logic is deterministic and testable.
- Include perturbation functions:
  perturb_delayed_settlement(hours_delay) — shifts due_times later.
  perturb_large_withdrawal(account_id, amount) — reduces a cash position.
  Both must NOT mutate the base dataset in place; return a new perturbed copy.
- No external dependencies beyond the standard library.

Must satisfy: AC-01 (item 3, missing/malformed account handling — include an
optional `simulate_missing_account=False` flag), AC-05 (item 3, overdue
flag support), AC-12/AC-13 (perturbation functions, item 3 — output must be
clearly separable from baseline, e.g. returned as a distinct dict, never
mutating the original).
```

---

## 2. tools.py
**Depends on:** mock_data.py
**Implements:** shared tool-calling functions used by Forecasting Agent, Funding Recommendation Agent, Alerting Agent

```
Write a Python module `tools.py` defining callable "tools" for agentic use in
a treasury liquidity system, built on top of mock_data.py.

Requirements:
- compute_liquidity_gap(account_id) -> dict with account_id, gap_amount
  (positive = shortfall, negative/zero = surplus), currency. Returns
  gap_amount="unknown" if underlying data is unavailable (AC-03 item 3).
- get_available_funding_sources() -> list of dicts (source_name, currency,
  available_amount) — mock funding facilities (e.g. intraday credit line,
  repo facility, FX swap line) for Funding Recommendation Agent to reference;
  must be the single source of truth so recommendations can be validated
  against it (AC-08 item 3 — no hallucinated sources).
- check_threshold_breach(metric_name, value, threshold_config) -> dict with
  breached (bool), severity, metric_name, value, threshold — pulls per
  account/currency threshold from threshold_config dict rather than a global
  constant (AC-10).
- Each function must have a clear docstring and type hints so it can be
  wired into an OpenAI function-calling / tool schema later if needed.
- Include simple unit-testable behavior: pure functions, no hidden state.
```

---

## 3. cash_position_agent.py
**Depends on:** mock_data.py
**Implements:** AC-01, AC-02, AC-03, AC-04, AC-05, AC-06

```
Write a Python module `cash_position_agent.py` implementing the "Cash &
Position Aggregator Agent" for a treasury liquidity system.

Requirements:
- Function aggregate_positions() that calls all six mock_data.py getters and
  returns ONE combined JSON-serializable dict with keys: cash_positions,
  nostro_by_currency (grouped/summed by currency), funding_gaps,
  collateral_movements, settlement_timeline (sorted ascending by due_time,
  each item flagged "overdue": true/false relative to mock_data.now()),
  market_indicators (each flagged "market_condition": "stressed"/"normal"
  relative to its threshold_reference).
- This agent does NOT call an LLM — it's pure data aggregation/transformation
  in Python, per the SDD.
- Handle missing/malformed data per-item (mark that item "status":
  "unavailable") without failing the whole aggregation (AC-01 item 3,
  AC-04 item 3, AC-06 item 3).
- nostro_by_currency must correctly sum multiple accounts sharing a currency,
  and omit currencies with zero reporting accounts (AC-02 items 2-3).
- Settlement timeline must retain duplicate due_times, not deduplicate them
  (AC-05 item 2).
- Return type: single dict matching the schema above, ready to pass directly
  into forecasting_agent.py.
```

---

## 4. forecasting_agent.py
**Depends on:** cash_position_agent.py
**Implements:** AC-07

```
Write a Python module `forecasting_agent.py` implementing the "Liquidity
Forecasting Agent," using the structured-output LLM pattern from the shared
call_llm() helper (see core pattern above — same JSON-mode style as
goal_task_list.py's planner()).

Requirements:
- Function forecast_shortfall(aggregated_positions: dict) -> dict.
- System prompt instructs the model: given aggregated cash/nostro/funding-gap/
  settlement data, return JSON exactly shaped as:
  {"shortfall_projected": true/false, "amount": <number or null>,
   "currency": <string or null>, "estimated_time_to_breach_minutes":
   <number or null>, "rationale": <short string>}
- Pass a compact JSON summary of aggregated_positions as the user prompt.
- Wrap the call_llm() invocation in try/except; on JSONDecodeError or missing
  keys, retry once; on second failure return
  {"error": "forecast_unavailable", "detail": <reason>} instead of raising
  (AC-07 item 3).
- Validate the parsed response against the exact schema above before
  returning it; raise/flag a schema-mismatch error object if it doesn't match
  (AC-07 item 4).
- Include a docstring noting this reuses the goal_task_list.py structured
  planner pattern.
```

---

## 5. funding_recommendation_agent.py
**Depends on:** forecasting_agent.py, tools.py
**Implements:** AC-08

```
Write a Python module `funding_recommendation_agent.py` implementing the
"Funding Recommendation Agent," ReAct-style: reason over the forecast and
available funding sources before recommending.

Requirements:
- Function recommend_action(forecast: dict) -> dict.
- If forecast["shortfall_projected"] is False, return
  {"action_needed": false, "recommendation": null} immediately — do not call
  the LLM (AC-08 item 2, avoids fabricated recommendations).
- Otherwise, call tools.get_available_funding_sources(), pass both the
  forecast and the funding sources list to the LLM via call_llm(), with a
  system prompt requiring the model to pick ONLY from the provided source
  names and return JSON:
  {"action_needed": true, "recommended_source": <must be one of the provided
  source_name values>, "amount": <number>, "currency": <string>,
  "rationale": <short string>}
- After parsing, validate recommended_source against the actual list from
  tools.py; if it doesn't match any real source, treat as an error and
  return {"action_needed": true, "error": "invalid_source_hallucinated"}
  rather than passing it through (AC-08 item 3).
- Wrap in try/except for malformed JSON, log the failure, return an error
  object rather than crashing (AC-08 item 4).
```

---

## 6. alerting_agent.py
**Depends on:** tools.py, cash_position_agent.py
**Implements:** AC-09, AC-10

```
Write a Python module `alerting_agent.py` implementing the "Alerting Agent."
This agent does NOT need an LLM call — it's deterministic threshold logic
using tools.check_threshold_breach().

Requirements:
- Function evaluate_alerts(aggregated_positions: dict, threshold_config: dict,
  previous_alert_state: dict) -> tuple(new_alerts: list, cleared_alerts: list,
  updated_alert_state: dict).
- For each relevant metric (funding gap per account, nostro balance per
  currency, market indicator), look up its threshold via threshold_config;
  if missing, skip alerting for it and add a warning to a returned
  `config_gaps` list rather than guessing a default silently (AC-09 item 4,
  AC-10 item 2 — apply a documented fallback default ONLY if one exists in
  threshold_config under a "default" key, otherwise skip+warn).
- If a metric breaches and wasn't previously breached (per
  previous_alert_state), emit a new alert with metric, account, threshold,
  actual value (AC-09 item 1).
- If a metric no longer breaches but was previously alerting, emit a
  clear/resolution event, not a duplicate ongoing alert (AC-09 item 3).
- If a metric stays within threshold and wasn't alerting, do nothing for it
  (AC-09 item 2).
- Reject/skip threshold_config entries with negative values, logging a
  validation error (AC-10 item 3).
- Return updated_alert_state so the caller can pass it into the next cycle.
```

---

## 7. stress_scenario_agent.py (Bonus)
**Depends on:** mock_data.py, forecasting_agent.py, alerting_agent.py
**Implements:** AC-12, AC-13

```
Write a Python module `stress_scenario_agent.py` implementing the "Stress
Scenario Agent" (bonus feature).

Requirements:
- Function run_delayed_settlement_scenario(hours_delay: int) -> dict: calls
  mock_data.perturb_delayed_settlement(hours_delay) to get perturbed data,
  re-aggregates via cash_position_agent-style logic (reuse or re-import),
  re-runs forecast_shortfall() on the perturbed aggregation, and returns
  {"scenario": "delayed_settlement", "hours_delay": hours_delay,
   "simulated": true, "forecast": <result>}.
- Function run_large_withdrawal_scenario(account_id: str, amount: float) ->
  dict: calls mock_data.perturb_large_withdrawal(), re-aggregates, re-runs
  both forecast_shortfall() and alerting_agent.evaluate_alerts() on the
  perturbed data, and returns {"scenario": "large_withdrawal",
  "account_id": account_id, "amount": amount, "simulated": true,
  "forecast": <result>, "alerts": <result>}.
- Every returned dict MUST include "simulated": true at the top level so
  callers can never mistake this for live data (AC-12 item 3, AC-13 item 3).
- Both functions must operate on perturbed copies only — never mutate the
  real mock_data state (relies on mock_data.py's non-mutating perturbation
  functions).
```

---

## 8. guardrails.py
**Depends on:** none (pure functions)
**Implements:** AC-16

```
Write a Python module `guardrails.py` implementing a guardrail check for
LLM-generated commentary text in a treasury liquidity system.

Requirements:
- Function validate_commentary(commentary_text: str, source_data: dict) ->
  dict with {"passed": bool, "issues": [list of strings]}.
- Extract numeric figures from commentary_text (regex is fine for this demo
  scope) and check each against the numeric values present anywhere in
  source_data (flattened). Any commentary number with no match in
  source_data is added to "issues" and fails the check (AC-16 items 1-2).
- Include a simple directional consistency check: if source_data indicates
  a forecast shortfall, but commentary_text contains phrases implying "no
  concern"/"healthy" (or vice versa), flag it as an issue (AC-16 item 3).
  Keep this check simple/keyword-based — this is a demo, not a production
  NLP system.
- Function should be pure and independently testable with hardcoded
  commentary_text + source_data examples.
```

---

## 9. commentary_agent.py
**Depends on:** guardrails.py, forecasting_agent.py, alerting_agent.py
**Implements:** AC-11

```
Write a Python module `commentary_agent.py` implementing the "Commentary
Agent," using the shared call_llm() structured-output pattern.

Requirements:
- Function generate_commentary(aggregated_positions: dict, forecast: dict,
  active_alerts: list) -> dict.
- System prompt: write a short, client-readable governance commentary
  (3-5 sentences) summarizing current liquidity position, referencing the
  actual forecast/shortfall figures and any active alerts, in JSON:
  {"commentary": <string>}.
- If forecast["shortfall_projected"] is False and active_alerts is empty,
  the system prompt must explicitly instruct the model to state liquidity is
  within normal range — not invent a concern (AC-11 item 3).
- After receiving the LLM response, run guardrails.validate_commentary() on
  it. If it fails, regenerate once with a stricter prompt reminding the model
  to only use provided figures; if it fails again, fall back to a Python
  f-string templated summary built directly from forecast/alerts data
  (AC-11 items 2 and 4 — LLM failure fallback).
- Return {"commentary": <final text>, "source": "llm" | "template_fallback",
  "guardrail_passed": bool}.
```

---

## 10. eval_harness.py
**Depends on:** all agent modules
**Implements:** AC-14, AC-15

```
Write a Python module `eval_harness.py` for testing the treasury agent
pipeline end-to-end on synthetic data.

Requirements:
- Function run_schema_validation_suite() that calls each LLM-backed agent
  (forecasting_agent, funding_recommendation_agent, commentary_agent) on a
  handful of representative mock_data scenarios and checks the response
  matches its documented JSON schema; reports a pass rate (AC-14).
- Function run_latency_check() that times a full evaluate_alerts() cycle
  against a mock breach event and asserts it completes within a 5-second
  budget, logging a failure if not (AC-15).
- Function run_full_report() that runs both suites above plus a basic
  end-to-end orchestrator run (import orchestrator.py once it exists) and
  prints a summary: {"json_validity_pass_rate": ..., "latency_check_passed":
  ..., "failures": [...]}.
- Keep this runnable standalone via `python eval_harness.py` for quick
  demo-prep sanity checks.
```

---

## 11. orchestrator.py
**Depends on:** cash_position_agent.py, forecasting_agent.py, funding_recommendation_agent.py, alerting_agent.py, commentary_agent.py, stress_scenario_agent.py
**Implements:** AC-17, AC-18 (TBD budget values — flag in code, see note below)

```
Write a Python module `orchestrator.py` implementing the Planner-Executor-
Synthesizer pipeline that ties every agent together, mirroring the pattern
from this workspace's Planner-Executor-Synthesizer Pipeline exercise.

Requirements:
- Function run_pipeline(threshold_config: dict, previous_alert_state: dict =
  None) -> dict that, in order: (1) calls cash_position_agent.aggregate_
  positions(), (2) calls forecasting_agent.forecast_shortfall(), (3) calls
  funding_recommendation_agent.recommend_action(), (4) calls alerting_agent.
  evaluate_alerts(), (5) calls commentary_agent.generate_commentary(), and
  returns a single combined result dict with all outputs plus a "run_
  timestamp".
- Log every step (agent name, timestamp, brief input summary, brief output
  summary) to a list or simple log file, including any retries/failures
  (AC-17 items 1-3).
- Wrap each step in try/except: if one agent step fails, log it, substitute
  a clearly marked degraded/error placeholder for that step's output, and
  CONTINUE the pipeline rather than aborting the whole run (AC-18 item 3).
- Add a module-level constant block at the top:
  DEMO_LATENCY_BUDGET_SECONDS = None  # TODO: set from specifications_document.md
  DEMO_COST_BUDGET_USD = None  # TODO: set from specifications_document.md
  with a comment noting these are currently TBD per acceptance_criteria.md
  AC-18, and should be filled in once the SDD defines them.
- Include an optional convenience function run_stress_scenario_pipeline(
  scenario_name, **kwargs) that calls stress_scenario_agent functions and
  returns their output clearly separated from run_pipeline()'s live output.
```

---

## 12. main.py (demo entrypoint)
**Depends on:** orchestrator.py
**Implements:** end-to-end demo run for client presentation

```
Write a Python script `main.py` as the live-demo entrypoint for the treasury
liquidity agent system.

Requirements:
- Define a sample threshold_config dict covering the mock accounts/currencies
  from mock_data.py.
- Call orchestrator.run_pipeline(threshold_config) and pretty-print the
  result (json.dumps with indent=2), including the commentary text clearly
  separated at the end so it reads well live in front of a client.
- Add a simple CLI flag or prompt to optionally trigger one of the stress
  scenarios (delayed settlement / large withdrawal) via orchestrator.
  run_stress_scenario_pipeline(), printing its output clearly labeled
  "[SIMULATION]" so it's never confused with the live run above it.
- Keep output terminal-readable — this is what runs on-screen during the
  client demo.
```

---

## Build Order Checklist

- [ ] 1. mock_data.py
- [ ] 2. tools.py
- [ ] 3. cash_position_agent.py
- [ ] 4. forecasting_agent.py
- [ ] 5. funding_recommendation_agent.py
- [ ] 6. alerting_agent.py
- [ ] 7. stress_scenario_agent.py (bonus)
- [ ] 8. guardrails.py
- [ ] 9. commentary_agent.py
- [ ] 10. eval_harness.py
- [ ] 11. orchestrator.py
- [ ] 12. main.py

**Before running eval_harness/orchestrator for real:** fill in
`DEMO_LATENCY_BUDGET_SECONDS` and `DEMO_COST_BUDGET_USD` in orchestrator.py —
these are the AC-18 gap flagged in acceptance_criteria.md.