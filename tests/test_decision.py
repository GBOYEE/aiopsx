import pytest
from aiopsx.agents.decision_agent import DecisionAgent

def test_decide_low_severity_low_risk():
    perms = {"tools": {"echo": {"risk": "low"}}}
    agent = DecisionAgent(perms)
    diagnosis = {"severity": "low", "suggested_action": {"tool": "echo", "args": {"cmd": "hi"}}}
    result = agent.decide(diagnosis)
    assert result["auto"] is True
    assert result["action"]["tool"] == "echo"

def test_decide_medium_severity_high_risk():
    perms = {"tools": {"shell": {"risk": "high"}}}
    agent = DecisionAgent(perms)
    diagnosis = {"severity": "medium", "suggested_action": {"tool": "shell", "args": {"cmd": "whoami"}}}
    result = agent.decide(diagnosis)
    assert result["auto"] is False
    assert result["reason"] == "requires approval due to severity/risk"

def test_decide_high_severity_low_risk():
    perms = {"tools": {"disk_clean": {"risk": "low"}}}
    agent = DecisionAgent(perms)
    diagnosis = {"severity": "high", "suggested_action": {"tool": "disk_clean", "args": {"limit_mb": 500}}}
    result = agent.decide(diagnosis)
    assert result["auto"] is False  # high severity requires approval even if tool low risk

def test_decide_unknown_tool():
    perms = {}
    agent = DecisionAgent(perms)
    diagnosis = {"severity": "low", "suggested_action": {"tool": "unknown", "args": {}}}
    result = agent.decide(diagnosis)
    assert result["action"] is None or result["action"]["tool"] == "unknown"
