from __future__ import annotations

import json
import time
from typing import Any, Dict, List

from cash_position_agent import aggregate_positions
from forecasting_agent import forecast_shortfall
from funding_recommendation_agent import recommend_action
from alerting_agent import evaluate_alerts
from commentary_agent import generate_commentary
from orchestrator import run_pipeline


def run_schema_validation_suite() -> Dict[str, Any]:
    aggregated = aggregate_positions()
    forecast = forecast_shortfall(aggregated)
    recommendation = recommend_action(forecast)
    alerts, cleared, state = evaluate_alerts(aggregated, {"funding_gap": 100000.0}, previous_alert_state={})
    commentary = generate_commentary(aggregated, forecast, alerts)
    checks = [forecast, recommendation, commentary]
    failures = []
    for index, payload in enumerate(checks):
        if not isinstance(payload, dict):
            failures.append(f"check_{index}: invalid output")
    return {"pass_rate": 1.0 if not failures else 0.0, "failures": failures}


def run_latency_check() -> Dict[str, Any]:
    start = time.perf_counter()
    aggregated = aggregate_positions()
    evaluate_alerts(aggregated, {"funding_gap": 100000.0}, previous_alert_state={})
    elapsed = time.perf_counter() - start
    return {"passed": elapsed < 5.0, "elapsed_seconds": round(elapsed, 3)}


def run_full_report() -> Dict[str, Any]:
    schema_suite = run_schema_validation_suite()
    latency_result = run_latency_check()
    orchestrated = run_pipeline({"funding_gap": 100000.0})
    return {"json_validity_pass_rate": schema_suite["pass_rate"], "latency_check_passed": latency_result["passed"], "failures": schema_suite["failures"], "orchestrator_output": orchestrated}


if __name__ == "__main__":
    print(json.dumps(run_full_report(), indent=2))
