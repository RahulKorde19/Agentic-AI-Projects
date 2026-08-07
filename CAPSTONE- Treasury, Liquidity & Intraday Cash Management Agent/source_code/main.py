from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from orchestrator import run_pipeline, run_stress_scenario_pipeline


def _read_markdown(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _build_payload(live_result: Dict[str, Any], simulation_result: Dict[str, Any]) -> Dict[str, Any]:
    markdown_docs = {
        "README.md": _read_markdown(Path(__file__).with_name("README.md")),
    }

    live_summary = live_result.get("forecast", {})
    recommendation = live_result.get("recommendation", {})
    alerts = live_result.get("alerts", [])
    commentary = live_result.get("commentary", {})

    return {
        "generated_at": live_result.get("run_timestamp"),
        "project": {
            "title": "Treasury Liquidity & Intraday Cash Management Agent",
            "summary": "A capstone demo showing how an agentic workflow can monitor cash positions, forecast liquidity shortfalls, recommend funding, trigger alerts, and generate governance commentary.",
            "what_it_demonstrates": [
                "Structured treasury data aggregation from mock cash, nostro, collateral, and settlement data.",
                "Pipeline orchestration across forecasting, funding, alerting, and commentary agents.",
                "Guardrails and graceful fallbacks when model responses are unavailable or schema-invalid.",
                "A polished frontend experience that turns backend reasoning into a recruiter-friendly demo."
            ],
            "learning_highlights": [
                "Prompted LLMs for JSON-structured treasury reasoning.",
                "Used modular agents that can be swapped for real market data or production services.",
                "Built a resilient orchestration loop with translation from agent output to visible business actions.",
                "Connected backend analysis to a presentation layer for stakeholder storytelling."
            ],
            "documentation": markdown_docs,
        },
        "live": {
            "status": "live_baseline",
            "summary": "This is the baseline run for the treasury liquidity workflow.",
            "snapshot": {
                "shortfall_projected": live_summary.get("shortfall_projected", False),
                "forecast_amount": live_summary.get("amount"),
                "forecast_currency": live_summary.get("currency"),
                "estimated_time_to_breach_minutes": live_summary.get("estimated_time_to_breach_minutes"),
                "recommended_source": recommendation.get("recommended_source"),
                "recommended_amount": recommendation.get("amount"),
                "alert_count": len(alerts),
                "commentary": commentary.get("commentary", ""),
                "guardrail_passed": commentary.get("guardrail_passed", False),
                "agent_count": len(live_result.get("logs", [])),
            },
            "aggregated_positions": live_result.get("aggregated_positions", {}),
            "forecast": live_summary,
            "recommendation": recommendation,
            "alerts": alerts,
            "alert_state": live_result.get("alert_state", {}),
            "commentary": commentary,
            "logs": live_result.get("logs", []),
            "raw_payload": live_result,
        },
        "simulation": {
            "status": "stress_test",
            "summary": "A stress scenario shows how the workflow behaves when settlement timing becomes delayed or funding demand spikes.",
            "scenario": simulation_result,
        },
    }


def _write_payload(payload: Dict[str, Any]) -> None:
    output_path = Path(__file__).with_name("demo_data.json")
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the treasury liquidity demo")
    parser.add_argument("--scenario", choices=["delayed_settlement", "large_withdrawal"], default=None)
    parser.add_argument("--hours-delay", type=int, default=2)
    parser.add_argument("--account-id", default="acct-001")
    parser.add_argument("--amount", type=float, default=500000.0)
    args = parser.parse_args()

    threshold_config = {
        "funding_gap": 100000.0,
        "repo_rate_spread": 0.4,
        "fx_volatility": 0.2,
    }

    live_result = run_pipeline(threshold_config)

    if args.scenario:
        simulation_result = run_stress_scenario_pipeline(
            args.scenario,
            hours_delay=args.hours_delay,
            account_id=args.account_id,
            amount=args.amount,
        )
    else:
        simulation_result = run_stress_scenario_pipeline("delayed_settlement", hours_delay=args.hours_delay)

    payload = _build_payload(live_result, simulation_result)
    _write_payload(payload)

    print("[LIVE RUN]")
    print(json.dumps(live_result, indent=2))
    print("\n[SIMULATION]")
    print(json.dumps(simulation_result, indent=2))
    print(f"\nWrote frontend payload to {Path(__file__).with_name('demo_data.json')}")


if __name__ == "__main__":
    main()
