from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from guardrails import validate_commentary


def call_llm(system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"commentary": "Liquidity remains within normal range based on the structured input snapshot."}

    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            timeout=60,
        )
        content = (response.choices[0].message.content or "").strip()
        if not content:
            return {"commentary": "Liquidity remains under review."}
        return {"commentary": content}
    except Exception:
        return {"commentary": "Liquidity remains under review."}


def generate_commentary(aggregated_positions: Dict[str, Any], forecast: Dict[str, Any], active_alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate governance commentary and validate it via guardrails."""
    if not forecast.get("shortfall_projected") and not active_alerts:
        system_prompt = "Write a 3-5 sentence governance commentary stating liquidity is within normal range. Use only provided figures and no fabricated concerns."
    else:
        system_prompt = "Write a short governance commentary using only provided figures. Mention the forecast and active alerts clearly."

    user_prompt = json.dumps({"aggregated_positions": aggregated_positions, "forecast": forecast, "active_alerts": active_alerts})
    try:
        response = call_llm(system_prompt, user_prompt)
    except Exception:
        response = {"commentary": "Liquidity remains under review. A fallback summary is being used because the LLM response was unavailable."}

    commentary = response.get("commentary", "")
    guardrail_result = validate_commentary(commentary, {"forecast": forecast, "alerts": active_alerts, "aggregated": aggregated_positions})
    if guardrail_result["passed"]:
        return {"commentary": commentary, "source": "llm", "guardrail_passed": True}
    fallback_commentary = f"Liquidity status: forecast shortfall={'yes' if forecast.get('shortfall_projected') else 'no'}; active alerts={len(active_alerts)}."
    return {"commentary": fallback_commentary, "source": "template_fallback", "guardrail_passed": False}
