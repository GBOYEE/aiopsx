import pytest
from aiopsx.agents.diagnosis_agent import DiagnosisAgent

def test_rule_based_high_cpu():
    agent = DiagnosisAgent()
    event = {"type": "HIGH_CPU", "value": 95}
    diag = agent._rule_based_diagnosis(event)
    assert diag["cause"] == "CPU overload"
    assert diag["severity"] == "high"
    assert diag["suggested_action"]["tool"] == "shell"

def test_rule_based_high_memory():
    agent = DiagnosisAgent()
    event = {"type": "HIGH_MEMORY", "value": 98}
    diag = agent._rule_based_diagnosis(event)
    assert diag["cause"] == "Memory pressure"
    assert diag["severity"] == "high"

def test_rule_based_high_disk():
    agent = DiagnosisAgent()
    event = {"type": "HIGH_DISK", "value": 95}
    diag = agent._rule_based_diagnosis(event)
    assert diag["cause"] == "Disk full"
    assert diag["suggested_action"]["tool"] == "disk_clean"

def test_rule_based_unknown():
    agent = DiagnosisAgent()
    event = {"type": "UNKNOWN"}
    diag = agent._rule_based_diagnosis(event)
    assert diag["cause"] == "unknown"
    assert diag["severity"] == "medium"
