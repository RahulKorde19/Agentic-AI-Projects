You are a senior AI systems architect. Using product_requirements_document.md
as the source of truth, generate a complete technical Specifications Document
(SDD) in Markdown and save it as `specifications_document.md`.

CONTEXT
Stack: Python, OpenAI API (chat.completions, JSON mode / structured outputs,
function/tool calling), synthetic/mock data (no live bank integrations).
Reuse patterns already implemented in this workspace's prior exercises —
treat them as proven building blocks to compose, not to reinvent:
- Goal → Task-List Decomposition (JSON-mode structured planning, e.g.
  goal_task_list.py) → reuse this pattern for shortfall forecasting and
  funding-action recommendation output.
- Planner-Executor-Synthesizer Pipeline → use as the orchestration backbone:
  Planner breaks "assess liquidity position" into sub-tasks, Executor agents
  each own one data domain (cash, nostro, collateral, settlement, market),
  Synthesizer merges results into the governance commentary.
- Reactive Supportive Triage Agent / Deliberative ReAct Agent with Tools →
  model for the Alerting Agent's reason-then-act loop on threshold breaches.
- Multi-Tool Ops Assistant / Reusable Calculator Agent with Framework →
  pattern for tool-calling (e.g. a "compute_liquidity_gap" tool, a
  "get_fx_rate" tool).
- Chunk+Embed+Semantic Search / RAG Memory Agent with Chroma Vector Store →
  optional, for retrieving historical liquidity commentary or policy
  documents to ground the governance narrative.
- Agent with Short-term + Long-term Memory → for retaining today's intraday
  snapshots across the session so forecasts can reference "3 hours ago."
- Guardrailed Responder → apply to the Commentary Agent's output before it's
  shown to treasury teams (no fabricated numbers, cite source data only).
- Multi Metric Evaluation Harness / Grade Answer with LLM Judge → reuse to
  score forecast accuracy and alert precision against your synthetic dataset.

INSTRUCTIONS — Structure the SDD with these sections:

1. System Overview & Architecture Diagram (describe in text/ASCII — orchestrator
   + named agents + data flow)

2. Agent Roster — for each agent define:
   - Name / responsibility (single sentence)
   - Inputs / outputs (with example JSON shape, following the
     response_format={"type":"json_object"} pattern)
   - Which prior-exercise pattern it's built from
   - Tools it can call (name, purpose, input/output schema)

3. Orchestration Flow
   - Step-by-step trace of one full run: user/system trigger → Planner →
     parallel/sequential Executor agents → Synthesizer → Commentary/Alert
     output
   - How threshold breaches short-circuit into the Alerting Agent

4. Data Model
   - Schema for: cash position, nostro balance, funding gap, collateral
     movement, settlement obligation, market liquidity indicator
   - Since data is synthetic: describe the mock data generator (a Python
     module that produces realistic intraday time-series for each schema)

5. Structured Output Contracts
   - For every LLM call in the system, define the exact JSON schema expected
     back, matching the JSON-mode style from goal_task_list.py

6. Alerting & Thresholds
   - Configurable threshold model (per currency / account / metric)
   - Alert severity levels and escalation logic

7. Stress Scenario Simulation (bonus feature)
   - List simulated scenarios (delayed settlement, market volatility spike,
     large client withdrawal)
   - How each scenario perturbs the mock data feed and what agent(s) react

8. Governance Commentary Generation
   - Prompt strategy for turning structured agent outputs into a
     client-readable narrative (tone, length, what must always be cited)

9. Guardrails & Evaluation
   - Guardrail rules applied to any generated text
   - Evaluation harness: metrics tracked, LLM-judge rubric, how pass/fail is
     decided

10. Tech Stack & Dependencies (Python packages, OpenAI models used per agent
    and why, e.g. gpt-4o-mini for fast structured calls)

11. File/Folder Structure for source_code/ (map directly to the agent roster
    in section 2 — one module per agent, plus orchestrator.py,
    mock_data.py, tools.py, guardrails.py, eval_harness.py)

12. Non-Functional Considerations (latency budget for a live demo, error
    handling / fallback if an LLM call fails, cost per run estimate)

13. Traceability Matrix — map each PRD feature (from product_requirements_
    document.md) to the agent(s)/section(s) that implement it

STYLE
- Every agent and data contract must be concrete enough to code directly from
  — this doc is the bridge between the PRD and the source code.
- Prefer reusing an existing pattern over inventing a new one; note explicitly
  when a new pattern is genuinely needed and why.
- Keep it demo-scoped: this must be buildable and runnable within ~2 hours.