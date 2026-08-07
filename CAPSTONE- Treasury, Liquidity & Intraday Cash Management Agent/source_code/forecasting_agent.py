from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def call_llm(system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    """Use the workspace's structured-output pattern for JSON-mode LLM calls."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"shortfall_projected": True, "amount": 800000.0, "currency": "USD", "estimated_time_to_breach_minutes": 90, "rationale": "Synthetic fallback forecast: funding gap is widening."}

    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"shortfall_projected": True, "amount": 800000.0, "currency": "USD", "estimated_time_to_breach_minutes": 90, "rationale": "Synthetic fallback forecast: funding gap is widening."}


def _validate_forecast(payload: Dict[str, Any]) -> bool:
    expected_keys = {"shortfall_projected", "amount", "currency", "estimated_time_to_breach_minutes", "rationale"}
    if not isinstance(payload, dict):
        return False
    return expected_keys.issubset(payload.keys())


def forecast_shortfall(aggregated_positions: Dict[str, Any]) -> Dict[str, Any]:
    """Forecast whether liquidity is projected to breach, using the goal_task_list planner pattern."""
    summary = json.dumps(aggregated_positions, sort_keys=True)[:4000]
    system_prompt = "You are a treasury forecasting assistant. Return JSON with keys shortfall_projected, amount, currency, estimated_time_to_breach_minutes, rationale."
    user_prompt = f"Forecast the near-term liquidity risk from this aggregated treasury snapshot: {summary}"

    try:
        response = call_llm(system_prompt, user_prompt)
        if not _validate_forecast(response):
            raise ValueError("schema_mismatch")
        return response
    except Exception as exc:
        return {"error": "forecast_unavailable", "detail": str(exc)}
