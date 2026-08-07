from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Optional

from cash_position_agent import aggregate_positions
from forecasting_agent import forecast_shortfall
from funding_recommendation_agent import recommend_action
from alerting_agent import evaluate_alerts
from commentary_agent import generate_commentary
from stress_scenario_agent import run_delayed_settlement_scenario, run_large_withdrawal_scenario

DEMO_LATENCY_BUDGET_SECONDS = None  # TODO: set from specifications_document.md
DEMO_COST_BUDGET_USD = None  # TODO: set from specifications_document.md


def _log_step(agent_name: str, payload: Dict[str, Any], outcome: Dict[str, Any], logs: list) -> None:
    logs.append({
        "agent": agent_name,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "input_summary": json.dumps(payload)[:200],
        "output_summary": json.dumps(outcome)[:200],
    })


def run_pipeline(threshold_config: Optional[Dict[str, Any]] = None, previous_alert_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run the agent pipeline in a degraded, non-blocking fashion."""
    threshold_config = threshold_config or {"funding_gap": 100000.0}
    previous_alert_state = previous_alert_state or {}
    logs = []

    try:
        aggregated = aggregate_positions()
        _log_step("cash_position_agent", {"source": "mock_data"}, aggregated, logs)
    except Exception as exc:
        aggregated = {"error": "aggregation_unavailable", "detail": str(exc)}
        _log_step("cash_position_agent", {"source": "mock_data"}, aggregated, logs)

    try:
        forecast = forecast_shortfall(aggregated)
        _log_step("forecasting_agent", aggregated, forecast, logs)
    except Exception as exc:
        forecast = {"error": "forecast_unavailable", "detail": str(exc)}
        _log_step("forecasting_agent", aggregated, forecast, logs)

    try:
        recommendation = recommend_action(forecast)
        _log_step("funding_recommendation_agent", forecast, recommendation, logs)
    except Exception as exc:
        recommendation = {"action_needed": True, "error": f"recommendation_failed:{exc}"}
        _log_step("funding_recommendation_agent", forecast, recommendation, logs)

    try:
        alerts, cleared, state = evaluate_alerts(aggregated, threshold_config, previous_alert_state)
        _log_step("alerting_agent", {"threshold_config": threshold_config, "previous_alert_state": previous_alert_state}, {"alerts": alerts, "cleared": cleared, "state": state}, logs)
    except Exception as exc:
        alerts, cleared, state = [], [], {"error": str(exc)}
        _log_step("alerting_agent", {"threshold_config": threshold_config, "previous_alert_state": previous_alert_state}, {"alerts": alerts, "cleared": cleared, "state": state}, logs)

    try:
        commentary = generate_commentary(aggregated, forecast, alerts)
        _log_step("commentary_agent", {"forecast": forecast, "alerts": alerts}, commentary, logs)
    except Exception as exc:
        commentary = {"commentary": f"Commentary unavailable: {exc}", "source": "template_fallback", "guardrail_passed": False}
        _log_step("commentary_agent", {"forecast": forecast, "alerts": alerts}, commentary, logs)

    return {
        "run_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "aggregated_positions": aggregated,
        "forecast": forecast,
        "recommendation": recommendation,
        "alerts": alerts,
        "cleared_alerts": cleared,
        "alert_state": state,
        "commentary": commentary,
        "logs": logs,
    }


def run_stress_scenario_pipeline(scenario_name: str, **kwargs) -> Dict[str, Any]:
    if scenario_name == "delayed_settlement":
        return {"live_output": False, "simulation": run_delayed_settlement_scenario(kwargs.get("hours_delay", 2))}
    if scenario_name == "large_withdrawal":
        return {"live_output": False, "simulation": run_large_withdrawal_scenario(kwargs.get("account_id", "acct-001"), kwargs.get("amount", 500000.0))}
    return {"error": "unknown_scenario"}
