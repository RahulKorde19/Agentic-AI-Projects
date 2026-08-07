from __future__ import annotations

from typing import Any, Dict, List, Optional

from mock_data import get_funding_gaps


def compute_liquidity_gap(account_id: str) -> Dict[str, Any]:
    """Compute a simple funding-gap estimate for one account."""
    for entry in get_funding_gaps():
        if entry.get("account_id") == account_id:
            obligations = float(entry.get("obligations_due", 0) or 0)
            liquidity = float(entry.get("available_liquidity", 0) or 0)
            gap_amount = obligations - liquidity
            return {"account_id": account_id, "gap_amount": gap_amount, "currency": "USD"}
    return {"account_id": account_id, "gap_amount": "unknown", "currency": "USD"}


def get_available_funding_sources() -> List[Dict[str, Any]]:
    """Return the mock funding facilities the recommendation agent may use."""
    return [
        {"source_name": "Intraday Credit Line", "currency": "USD", "available_amount": 5000000.0},
        {"source_name": "Repo Facility", "currency": "USD", "available_amount": 2500000.0},
        {"source_name": "FX Swap Line", "currency": "EUR", "available_amount": 1500000.0},
    ]


def check_threshold_breach(metric_name: str, value: float, threshold_config: Dict[str, Any], account_id: Optional[str] = None, currency: Optional[str] = None) -> Dict[str, Any]:
    """Check whether a metric exceeds a configured threshold."""
    if isinstance(threshold_config, dict):
        if metric_name in threshold_config and isinstance(threshold_config[metric_name], (int, float)):
            threshold = float(threshold_config[metric_name])
        elif metric_name in threshold_config and isinstance(threshold_config[metric_name], dict):
            if account_id and currency and currency in threshold_config[metric_name].get(account_id, {}):
                threshold = float(threshold_config[metric_name][account_id][currency])
            elif "default" in threshold_config[metric_name]:
                threshold = float(threshold_config[metric_name]["default"])
            else:
                threshold = None
        else:
            threshold = None
    else:
        threshold = None

    if threshold is None:
        return {"breached": False, "severity": "info", "metric_name": metric_name, "value": value, "threshold": None}
    if threshold < 0:
        return {"breached": False, "severity": "invalid", "metric_name": metric_name, "value": value, "threshold": threshold}

    breached = value > threshold
    severity = "critical" if breached and value > threshold * 1.5 else "warning" if breached else "info"
    return {"breached": breached, "severity": severity, "metric_name": metric_name, "value": value, "threshold": threshold}
