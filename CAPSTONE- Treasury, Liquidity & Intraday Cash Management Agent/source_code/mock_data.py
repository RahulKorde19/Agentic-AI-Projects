from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, Dict, List


_FIXED_NOW = datetime(2026, 8, 6, 12, 0, 0)


def now() -> datetime:
    """Return the deterministic current time for the demo."""
    return _FIXED_NOW


def get_cash_positions() -> List[Dict[str, Any]]:
    return [
        {"account_id": "acct-001", "currency": "USD", "balance": 4500000.0, "timestamp": now().isoformat()},
        {"account_id": "acct-002", "currency": "EUR", "balance": 2800000.0, "timestamp": now().isoformat()},
        {"account_id": "acct-003", "currency": "GBP", "balance": 1200000.0, "timestamp": now().isoformat()},
        {"account_id": "acct-004", "currency": "USD", "balance": 900000.0, "timestamp": now().isoformat()},
    ]


def get_nostro_balances() -> List[Dict[str, Any]]:
    return [
        {"account_id": "nostro-001", "currency": "USD", "balance": 3200000.0, "correspondent_bank": "JP Morgan"},
        {"account_id": "nostro-002", "currency": "EUR", "balance": 1800000.0, "correspondent_bank": "BNP Paribas"},
        {"account_id": "nostro-003", "currency": "GBP", "balance": 960000.0, "correspondent_bank": "Barclays"},
        {"account_id": "nostro-004", "currency": "USD", "balance": 700000.0, "correspondent_bank": "Goldman Sachs"},
    ]


def get_funding_gaps() -> List[Dict[str, Any]]:
    return [
        {"account_id": "acct-001", "obligations_due": 5000000.0, "available_liquidity": 4500000.0, "timestamp": now().isoformat()},
        {"account_id": "acct-002", "obligations_due": 1800000.0, "available_liquidity": 2800000.0, "timestamp": now().isoformat()},
        {"account_id": "acct-003", "obligations_due": 1300000.0, "available_liquidity": 1200000.0, "timestamp": now().isoformat()},
    ]


def get_collateral_movements() -> List[Dict[str, Any]]:
    return [
        {"movement_id": "col-001", "direction": "in", "amount": 400000.0, "currency": "USD", "settlement_time": (now() + timedelta(hours=2)).isoformat()},
        {"movement_id": "col-002", "direction": "out", "amount": 150000.0, "currency": "EUR", "settlement_time": None},
        {"movement_id": "col-003", "direction": "in", "amount": 90000.0, "currency": "GBP", "settlement_time": (now() - timedelta(hours=1)).isoformat()},
    ]


def get_settlement_obligations() -> List[Dict[str, Any]]:
    return [
        {"obligation_id": "sett-001", "account_id": "acct-001", "amount": 1800000.0, "currency": "USD", "due_time": (now() + timedelta(hours=2)).isoformat()},
        {"obligation_id": "sett-002", "account_id": "acct-002", "amount": 700000.0, "currency": "EUR", "due_time": (now() + timedelta(hours=4)).isoformat()},
        {"obligation_id": "sett-003", "account_id": "acct-003", "amount": 220000.0, "currency": "GBP", "due_time": (now() - timedelta(hours=1)).isoformat()},
        {"obligation_id": "sett-004", "account_id": "acct-001", "amount": 650000.0, "currency": "USD", "due_time": (now() + timedelta(hours=2)).isoformat()},
    ]


def get_market_indicators() -> List[Dict[str, Any]]:
    return [
        {"indicator_name": "repo_rate_spread", "value": 0.55, "threshold_reference": 0.4, "timestamp": now().isoformat()},
        {"indicator_name": "fx_volatility", "value": 0.18, "threshold_reference": 0.2, "timestamp": now().isoformat()},
    ]


def perturb_delayed_settlement(hours_delay: int) -> Dict[str, Any]:
    perturbed = {
        "cash_positions": get_cash_positions(),
        "nostro_balances": get_nostro_balances(),
        "funding_gaps": get_funding_gaps(),
        "collateral_movements": get_collateral_movements(),
        "settlement_obligations": [],
        "market_indicators": get_market_indicators(),
        "scenario": "delayed_settlement",
        "hours_delay": hours_delay,
    }
    for item in get_settlement_obligations():
        due_time = datetime.fromisoformat(item["due_time"]) + timedelta(hours=hours_delay)
        new_item = deepcopy(item)
        new_item["due_time"] = due_time.isoformat()
        perturbed["settlement_obligations"].append(new_item)
    return perturbed


def perturb_large_withdrawal(account_id: str, amount: float) -> Dict[str, Any]:
    perturbed = {
        "cash_positions": [],
        "nostro_balances": get_nostro_balances(),
        "funding_gaps": get_funding_gaps(),
        "collateral_movements": get_collateral_movements(),
        "settlement_obligations": get_settlement_obligations(),
        "market_indicators": get_market_indicators(),
        "scenario": "large_withdrawal",
        "account_id": account_id,
        "amount": amount,
    }
    for item in get_cash_positions():
        new_item = deepcopy(item)
        if new_item["account_id"] == account_id:
            new_item["balance"] = max(0.0, new_item["balance"] - amount)
        perturbed["cash_positions"].append(new_item)
    return perturbed
