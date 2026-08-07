from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

from tools import check_threshold_breach
from cash_position_agent import aggregate_positions


logging.basicConfig(level=logging.INFO)


def evaluate_alerts(aggregated_positions: Dict[str, Any], threshold_config: Dict[str, Any], previous_alert_state: Dict[str, Any] | None = None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    """Evaluate breach conditions and return new/cleared alerts plus updated state."""
    previous_alert_state = previous_alert_state or {}
    new_alerts: List[Dict[str, Any]] = []
    cleared_alerts: List[Dict[str, Any]] = []
    updated_state: Dict[str, Any] = {}
    config_gaps: List[Dict[str, Any]] = []

    active_metrics = {}
    for entry in aggregated_positions.get("funding_gaps", []):
        if not isinstance(entry, dict):
            continue
        account_id = entry.get("account_id")
        gap = entry.get("available_liquidity", 0) - entry.get("obligations_due", 0)
        result = check_threshold_breach("funding_gap", gap, threshold_config, account_id=account_id, currency="USD")
        if not result.get("threshold"):
            config_gaps.append({"metric": "funding_gap", "account_id": account_id, "reason": "missing_threshold"})
        elif result.get("breached"):
            active_metrics[f"funding_gap:{account_id}"] = {"metric": "funding_gap", "account_id": account_id, "threshold": result["threshold"], "value": result["value"]}

    for entry in aggregated_positions.get("market_indicators", []):
        if not isinstance(entry, dict):
            continue
        metric_name = entry.get("indicator_name", "market_indicator")
        value = entry.get("value", 0)
        result = check_threshold_breach(metric_name, value, threshold_config, account_id=None, currency=None)
        if not result.get("threshold"):
            config_gaps.append({"metric": metric_name, "reason": "missing_threshold"})
        elif result.get("breached"):
            active_metrics[f"indicator:{metric_name}"] = {"metric": metric_name, "threshold": result["threshold"], "value": result["value"]}

    for metric_key, metric_value in active_metrics.items():
        if previous_alert_state.get(metric_key) != metric_value:
            new_alerts.append({"metric": metric_value["metric"], "account": metric_value.get("account_id"), "threshold": metric_value["threshold"], "actual_value": metric_value["value"]})

    for key in previous_alert_state:
        if key not in active_metrics:
            cleared_alerts.append({"metric": key, "status": "cleared"})

    updated_state = dict(active_metrics)
    return new_alerts, cleared_alerts, {"alerts": updated_state, "config_gaps": config_gaps}
