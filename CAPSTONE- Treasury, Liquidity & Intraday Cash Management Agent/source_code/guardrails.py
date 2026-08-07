from __future__ import annotations

import re
from typing import Any, Dict, List


def validate_commentary(commentary_text: str, source_data: Dict[str, Any]) -> Dict[str, Any]:
    """Perform a lightweight guardrail check to ensure commentary uses only grounded numbers."""
    issues: List[str] = []
    numbers = re.findall(r"\d+(?:\.\d+)?", commentary_text)
    flattened_values = []

    def walk(value: Any) -> List[Any]:
        if isinstance(value, dict):
            values = []
            for item in value.values():
                values.extend(walk(item))
            return values
        if isinstance(value, list):
            values = []
            for item in value:
                values.extend(walk(item))
            return values
        if isinstance(value, (int, float)):
            return [value]
        return []

    flattened_values = [float(v) for v in walk(source_data)]
    for number in numbers:
        if float(number) not in flattened_values:
            issues.append(f"unmatched_number:{number}")

    if isinstance(source_data, dict) and source_data.get("forecast", {}).get("shortfall_projected") is True:
        if re.search(r"healthy|normal range|no concern", commentary_text, re.IGNORECASE):
            issues.append("directional_mismatch")
    elif isinstance(source_data, dict) and source_data.get("forecast", {}).get("shortfall_projected") is False:
        if re.search(r"tightening|shortfall|breach|concern", commentary_text, re.IGNORECASE):
            issues.append("directional_mismatch")

    return {"passed": not issues, "issues": issues}
