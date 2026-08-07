from __future__ import annotations

from typing import Any, Dict

import mock_data
from cash_position_agent import aggregate_positions
from forecasting_agent import forecast_shortfall
from alerting_agent import evaluate_alerts


def run_delayed_settlement_scenario(hours_delay: int) -> Dict[str, Any]:
    """Simulate delayed settlement and re-run the forecast."""
    perturbed = mock_data.perturb_delayed_settlement(hours_delay)
    aggregated = aggregate_positions({
        "cash_positions": perturbed["cash_positions"],
        "nostro_balances": perturbed["nostro_balances"],
        "funding_gaps": perturbed["funding_gaps"],
        "collateral_movements": perturbed["collateral_movements"],
        "settlement_obligations": perturbed["settlement_obligations"],
        "market_indicators": perturbed["market_indicators"],
    })
    return {"scenario": "delayed_settlement", "hours_delay": hours_delay, "simulated": True, "forecast": forecast_shortfall(aggregated)}


def run_large_withdrawal_scenario(account_id: str, amount: float) -> Dict[str, Any]:
    """Simulate a large withdrawal and re-run forecast plus alerts."""
    perturbed = mock_data.perturb_large_withdrawal(account_id, amount)
    aggregated = aggregate_positions({
        "cash_positions": perturbed["cash_positions"],
        "nostro_balances": perturbed["nostro_balances"],
        "funding_gaps": perturbed["funding_gaps"],
        "collateral_movements": perturbed["collateral_movements"],
        "settlement_obligations": perturbed["settlement_obligations"],
        "market_indicators": perturbed["market_indicators"],
    })
    new_alerts, cleared_alerts, updated_state = evaluate_alerts(aggregated, {"funding_gap": 100000.0}, previous_alert_state={})
    return {"scenario": "large_withdrawal", "account_id": account_id, "amount": amount, "simulated": True, "forecast": forecast_shortfall(aggregated), "alerts": {"new_alerts": new_alerts, "cleared_alerts": cleared_alerts, "updated_state": updated_state}}
