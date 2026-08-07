from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from tools import get_available_funding_sources


def call_llm(system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"action_needed": True, "recommended_source": "Intraday Credit Line", "amount": 750000.0, "currency": "USD", "rationale": "Synthetic fallback recommendation."}

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
        return {"action_needed": True, "recommended_source": "Intraday Credit Line", "amount": 750000.0, "currency": "USD", "rationale": "Synthetic fallback recommendation."}


def recommend_action(forecast: Dict[str, Any]) -> Dict[str, Any]:
    """Recommend a funding action from the available mock facilities."""
    if not forecast.get("shortfall_projected", False):
        return {"action_needed": False, "recommendation": None}

    sources = get_available_funding_sources()
    source_names = [source["source_name"] for source in sources]
    system_prompt = "You are a treasury funding assistant. Select a funding source only from the provided list and return JSON with action_needed, recommended_source, amount, currency, rationale."
    user_prompt = json.dumps({"forecast": forecast, "sources": sources})

    try:
        response = call_llm(system_prompt, user_prompt)
        if response.get("recommended_source") not in source_names:
            return {"action_needed": True, "error": "invalid_source_hallucinated"}
        return response
    except Exception as exc:
        return {"action_needed": True, "error": f"recommendation_failed:{exc}"}
