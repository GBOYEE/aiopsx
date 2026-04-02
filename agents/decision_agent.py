"""Decision Agent — maps diagnosis to action with approval policy."""
from typing import Dict, Any

class DecisionAgent:
    def __init__(self, permissions: Dict[str, Any]):
        self.permissions = permissions

    def decide(self, diagnosis: Dict[str, Any]) -> Dict[str, Any]:
        severity = diagnosis.get("severity", "medium").lower()
        action = diagnosis.get("suggested_action", {})
        tool = action.get("tool")
        risk = self._get_risk(tool)

        if severity == "low" and risk in ("low", "medium"):
            # Auto-execute if tool risk is low or medium (configurable)
            return {"action": action, "auto": True, "reason": "low severity"}
        elif severity in ("medium", "high") or risk in ("medium", "high"):
            # Require approval
            return {"action": action, "auto": False, "reason": "requires approval due to severity/risk"}
        else:
            # Block unknown
            return {"action": None, "auto": False, "reason": "blocked by policy"}

    def _get_risk(self, tool: str) -> str:
        if not tool:
            return "medium"
        return self.permissions.get("tools", {}).get(tool, {}).get("risk", "medium")
