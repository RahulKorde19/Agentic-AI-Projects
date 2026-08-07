# Acceptance Criteria — Treasury, Liquidity & Intraday Cash Management Agent

One AC block per user story in `user_stories.md`, same order and IDs.

---

### AC-01: Aggregate intraday cash positions
**Story reference:** US-01

1. **Given** mock intraday cash data exists for at least 3 accounts, **when** the Cash & Position Aggregator Agent runs, **then** it returns a single JSON object listing every account's current cash position with a timestamp.
2. **Given** two accounts share the same currency, **when** the aggregation runs, **then** their positions are both present individually and summed into a currency-level total.
3. **Given** one account's mock data is missing/malformed, **when** the aggregation runs, **then** that account is flagged as `"status": "unavailable"` in the output rather than causing the whole run to fail.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-02: Aggregate nostro balances across currencies
**Story reference:** US-02

1. **Given** nostro balances exist in at least 3 currencies, **when** the agent aggregates them, **then** the output JSON is keyed by currency code (e.g. `"USD"`, `"EUR"`).
2. **Given** a currency has multiple nostro accounts, **when** aggregation runs, **then** the currency total equals the sum of its accounts (verified in eval harness).
3. **Given** a currency has zero accounts reporting data, **when** aggregation runs, **then** it is omitted from the output rather than shown as a false zero.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-03: Track funding gaps in real time
**Story reference:** US-03

1. **Given** obligations due exceed available liquidity for an account, **when** the gap calculation runs, **then** the output reports a positive gap amount and the account ID.
2. **Given** available liquidity exceeds obligations due, **when** the gap calculation runs, **then** the gap amount is reported as 0 or negative (surplus), not omitted.
3. **Given** obligation data for an account is unavailable, **when** the gap calculation runs, **then** that account's gap is marked `"unknown"` rather than defaulting to 0.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-04: Monitor collateral movements
**Story reference:** US-04

1. **Given** an incoming and an outgoing collateral movement exist in the mock feed, **when** the agent processes them, **then** both appear in the output with direction (`in`/`out`) and amount.
2. **Given** a collateral movement has no settlement time, **when** processed, **then** it is still included but flagged `"settlement_time": null`.
3. **Given** the collateral feed is empty for the run, **when** the agent runs, **then** it returns an empty list, not an error.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-05: Track settlement obligations timeline
**Story reference:** US-05

1. **Given** multiple settlement obligations with different due-times, **when** the agent builds the timeline, **then** the output list is sorted ascending by due-time.
2. **Given** two obligations share the exact same due-time, **when** sorted, **then** both are retained in the output (no silent de-duplication).
3. **Given** an obligation has a due-time in the past relative to "now" in the mock clock, **when** the timeline builds, **then** it is flagged `"overdue": true`.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-06: View market liquidity indicators
**Story reference:** US-06

1. **Given** the mock market indicator feed returns a value, **when** the agent fetches it, **then** it is included in the aggregated output alongside internal positions.
2. **Given** the indicator value crosses a pre-defined "stressed market" reference level, **when** fetched, **then** the output includes a `"market_condition": "stressed"` flag.
3. **Given** the market indicator feed is unavailable, **when** the agent runs, **then** the rest of the aggregation still completes, with the market section marked unavailable.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-07: Forecast intraday liquidity shortfall
**Story reference:** US-07

1. **Given** aggregated position data showing a widening funding gap trend, **when** the Forecasting Agent runs, **then** it returns a JSON object with a projected shortfall amount, currency, and estimated time-to-breach.
2. **Given** the same input data is run twice, **when** compared, **then** the forecast direction (shortfall vs. no shortfall) is consistent (checked via eval harness, not exact-value match, since LLM output can vary slightly).
3. **Given** the LLM call returns malformed JSON, **when** parsing is attempted, **then** the agent retries once and, on second failure, returns a clearly marked error object instead of crashing the orchestrator.
4. **Given** valid output is returned, **when** validated, **then** it matches the exact schema defined in specifications_document.md section 5.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-08: Receive funding action recommendations
**Story reference:** US-08

1. **Given** the Forecasting Agent has projected a shortfall, **when** the Funding Recommendation Agent runs, **then** it returns at least one concrete recommended action (e.g. draw a specific facility, move collateral) referencing the actual shortfall amount.
2. **Given** no shortfall is forecast, **when** the agent runs, **then** it returns an explicit "no action needed" response rather than a fabricated recommendation.
3. **Given** the recommendation references a funding source, **when** validated, **then** that source must exist in the mock funding-sources data (no hallucinated sources).
4. **Given** the LLM response is malformed JSON, **when** parsing fails, **then** the agent handles it gracefully and logs the failure rather than passing bad data downstream.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-09: Get alerted on threshold breach
**Story reference:** US-09

1. **Given** a metric crosses its configured threshold in the mock data stream, **when** the Alerting Agent evaluates it, **then** an alert is generated referencing the metric, account, threshold, and actual value.
2. **Given** a metric stays within threshold, **when** evaluated, **then** no alert is generated for it.
3. **Given** a metric breaches threshold and later returns within range, **when** evaluated on the next cycle, **then** a resolution/clear event is generated (not a duplicate ongoing alert).
4. **Given** threshold configuration is missing for a given account/currency pair, **when** evaluated, **then** the agent skips alerting for it and logs a configuration-gap warning instead of guessing a default.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-10: Configure liquidity thresholds per account/currency
**Story reference:** US-10

1. **Given** a threshold config file/object defining limits per account and currency, **when** the Alerting Agent loads it, **then** each account/currency pair uses its own configured value, not a global default.
2. **Given** an account/currency pair has no explicit config, **when** loaded, **then** a documented fallback default is applied and logged as such.
3. **Given** an invalid threshold value (e.g. negative number) is present in config, **when** loaded, **then** the agent rejects that entry and logs a validation error rather than using it silently.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-11: Generate daily governance commentary
**Story reference:** US-11

1. **Given** aggregated positions, forecast, and any active alerts, **when** the Commentary Agent runs, **then** it produces a readable narrative that references the actual current shortfall/surplus figure.
2. **Given** the commentary is generated, **when** passed through Guardrails, **then** any number in the text is traceable to the structured input data, or the commentary is rejected/flagged for regeneration.
3. **Given** there are zero alerts and no forecast shortfall, **when** the agent runs, **then** the commentary explicitly states liquidity is within normal range rather than fabricating a concern.
4. **Given** the LLM call fails, **when** commentary generation is attempted, **then** the system falls back to a templated summary built directly from structured data rather than showing nothing.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-12 (Bonus): Simulate delayed settlement stress scenario
**Story reference:** US-12

1. **Given** the user triggers the "delayed settlement" scenario, **when** the Stress Scenario Agent runs, **then** it shifts one or more settlement obligations' due-times later in the mock data and re-runs the Forecasting Agent on the perturbed data.
2. **Given** the scenario is applied, **when** compared to the baseline forecast, **then** the resulting shortfall projection is measurably different (worse) than the unperturbed baseline.
3. **Given** the scenario run completes, **when** displayed, **then** the output is clearly labeled as a simulation, never mixed into live/baseline figures.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-13 (Bonus): Simulate large client withdrawal stress scenario
**Story reference:** US-13

1. **Given** the user triggers the "large withdrawal" scenario with a specified amount, **when** the Stress Scenario Agent runs, **then** it reduces the relevant account's mock cash position by that amount before re-running Forecasting and Alerting.
2. **Given** the withdrawal amount is large enough to breach a configured threshold, **when** the scenario runs, **then** the Alerting Agent fires a simulation-labeled alert.
3. **Given** the scenario run completes, **when** displayed, **then** it is clearly labeled as a simulation, never mixed into live/baseline figures.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-14: Structured outputs are always valid JSON
**Story reference:** US-14

1. **Given** any agent makes an LLM call, **when** the response is received, **then** it is parsed successfully against that agent's defined JSON schema in 100% of eval-harness test runs.
2. **Given** a response fails schema validation, **when** detected, **then** the eval harness logs it as a failure with the raw response for debugging, rather than the agent silently proceeding with bad data.
3. **Given** the eval harness runs its full test suite, **when** results are compiled, **then** a JSON-validity pass rate is reported as one of the tracked metrics.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] N/A — this story is itself the structured-output check
- [ ] Covered by at least one case in the evaluation harness

---

### AC-15: Alerts fire within 5 seconds of a breach
**Story reference:** US-15

1. **Given** a timestamped mock data point crosses a threshold, **when** the Alerting Agent's next evaluation cycle runs, **then** the alert timestamp is within 5 seconds of the breach timestamp.
2. **Given** multiple breaches occur simultaneously across accounts, **when** evaluated, **then** all resulting alerts are still generated within the same 5-second budget (no serial bottleneck).
3. **Given** the evaluation cycle itself takes longer than 5 seconds due to an LLM call delay, **when** measured, **then** this is logged as a latency-budget failure in the eval harness.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] N/A — non-functional/timing story
- [ ] Covered by at least one case in the evaluation harness

---

### AC-16: Guardrails prevent fabricated figures in commentary
**Story reference:** US-16

1. **Given** generated commentary text, **when** Guardrails scans it, **then** every numeric figure mentioned must match a value present in the structured input data supplied to the Commentary Agent.
2. **Given** a numeric figure in the commentary does NOT match any input value, **when** detected, **then** Guardrails blocks the output and triggers regeneration (or falls back to the templated summary).
3. **Given** the commentary makes a qualitative claim (e.g. "liquidity is tightening"), **when** scanned, **then** Guardrails checks it's directionally consistent with the forecast trend, not just checking numbers.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] Output validated against SDD structured-output contract
- [ ] Covered by at least one case in the evaluation harness

---

### AC-17: Agent decisions are logged for audit
**Story reference:** US-17

1. **Given** any agent produces an output (forecast, recommendation, alert, commentary), **when** it completes, **then** a log entry is written containing the agent name, timestamp, input summary, and output.
2. **Given** the orchestrator completes a full run, **when** logs are reviewed, **then** the sequence of agent calls can be reconstructed in order.
3. **Given** an agent call fails, **when** logged, **then** the failure and any retry are recorded, not just the eventual success.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] N/A — non-functional/logging story
- [ ] Covered by at least one case in the evaluation harness

---

### AC-18: Full demo run completes within budget
**Story reference:** US-18

1. **Given** a full orchestrated run (aggregation → forecast → recommendation → alert check → commentary), **when** timed end-to-end on mock data, **then** it completes within a target budget suitable for a live client demo (SDD to define exact seconds — flag as TBD if not yet set).
2. **Given** the run uses gpt-4o-mini for all LLM calls, **when** cost is estimated, **then** it stays within the per-run cost budget defined in specifications_document.md section 12 — TBD, needs SDD update if not yet defined.
3. **Given** any single agent in the pipeline fails, **when** the orchestrator handles it, **then** the overall run still completes (degraded, not blocked) so the demo doesn't hard-stop on one bad call.

**Definition of Done for this story:**
- [ ] All criteria above pass on synthetic test data
- [ ] N/A — non-functional/performance story
- [ ] Covered by at least one case in the evaluation harness

---

## Coverage Summary

| Story ID | # Criteria | Has Negative Case (Y/N) | Has Structured-Output Check (Y/N/N/A) |
|----------|-----------|--------------------------|-----------------------------------------|
| AC-01 | 3 | Y | Y |
| AC-02 | 3 | Y | Y |
| AC-03 | 3 | Y | Y |
| AC-04 | 3 | Y | Y |
| AC-05 | 3 | Y | Y |
| AC-06 | 3 | Y | Y |
| AC-07 | 4 | Y | Y |
| AC-08 | 4 | Y | Y |
| AC-09 | 4 | Y | Y |
| AC-10 | 3 | Y | Y |
| AC-11 | 4 | Y | Y |
| AC-12 | 3 | N (label check only) | Y |
| AC-13 | 3 | N (label check only) | Y |
| AC-14 | 3 | Y | N/A (self) |
| AC-15 | 3 | Y | N/A |
| AC-16 | 3 | Y | Y |
| AC-17 | 3 | Y | N/A |
| AC-18 | 3 | Y | N/A |

**Gaps flagged for SDD update:** AC-18 references exact latency and cost
budget values that specifications_document.md needs to state explicitly
(currently TBD).