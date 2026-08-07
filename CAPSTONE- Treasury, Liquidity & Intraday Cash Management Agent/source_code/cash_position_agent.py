from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from mock_data import get_cash_positions, get_collateral_movements, get_funding_gaps, get_market_indicators, get_nostro_balances, get_settlement_obligations, now


def aggregate_positions(data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Aggregate the synthetic treasury feed into one JSON-serializable dict."""
    if data is None:
        cash_positions = get_cash_positions()
        nostro_balances = get_nostro_balances()
        funding_gaps = get_funding_gaps()
        collateral_movements = get_collateral_movements()
        settlement_obligations = get_settlement_obligations()
        market_indicators = get_market_indicators()
    else:
        cash_positions = data.get("cash_positions", get_cash_positions())
        nostro_balances = data.get("nostro_balances", get_nostro_balances())
        funding_gaps = data.get("funding_gaps", get_funding_gaps())
        collateral_movements = data.get("collateral_movements", get_collateral_movements())
        settlement_obligations = data.get("settlement_obligations", get_settlement_obligations())
        market_indicators = data.get("market_indicators", get_market_indicators())

    normalized_cash = []
    for item in cash_positions:
        if not isinstance(item, dict) or not item.get("account_id"):
            normalized_cash.append({"status": "unavailable", "raw": item})
            continue
        normalized_cash.append({
            "account_id": item.get("account_id"),
            "currency": item.get("currency", "USD"),
            "balance": item.get("balance"),
            "timestamp": item.get("timestamp"),
        })

    nostro_by_currency: Dict[str, float] = defaultdict(float)
    for item in nostro_balances:
        if not isinstance(item, dict) or not item.get("currency"):
            continue
        nostro_by_currency[item["currency"]] += float(item.get("balance", 0) or 0)

    settlement_timeline = []
    for item in settlement_obligations:
        if not isinstance(item, dict):
            continue
        due_time = item.get("due_time")
        overdue = False
        if due_time:
            overdue = datetime.fromisoformat(due_time) < now()
        settlement_timeline.append({
            **item,
            "overdue": overdue,
        })
    settlement_timeline.sort(key=lambda entry: entry.get("due_time", ""))

    market_output = []
    for item in market_indicators:
        if not isinstance(item, dict):
            market_output.append({"status": "unavailable"})
            continue
        value = item.get("value")
        threshold = item.get("threshold_reference")
        market_output.append({
            "indicator_name": item.get("indicator_name"),
            "value": value,
            "threshold_reference": threshold,
            "market_condition": "stressed" if value is not None and threshold is not None and value > threshold else "normal",
        })

    return {
        "cash_positions": normalized_cash,
        "nostro_by_currency": {k: v for k, v in dict(nostro_by_currency).items() if v != 0},
        "funding_gaps": funding_gaps,
        "collateral_movements": collateral_movements,
        "settlement_timeline": settlement_timeline,
        "market_indicators": market_output,
    }
