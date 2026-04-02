import pytest
from unittest.mock import MagicMock, patch
from aiopsx.core.orchestrator import AIOpsOrchestrator
from aiopsx.agents.monitor_agent import MonitorAgent

@pytest.fixture
def mock_db_factory():
    def mock_session():
        session = MagicMock()
        session.add = MagicMock()
        session.commit = MagicMock()
        session.close = MagicMock()
        return session
    return lambda: mock_session()

@pytest.fixture
def perms():
    return {"tools": {"disk_clean": {"risk": "low"}}}

def test_orchestrator_init(mock_db_factory, perms):
    orch = AIOpsOrchestrator(db_session_factory=mock_db_factory, permissions=perms)
    assert orch.monitor is not None
    assert orch.diagnosis is not None
    assert orch.decision is not None
    assert orch.executor is not None

def test_cycle_no_event(mock_db_factory, perms):
    orch = AIOpsOrchestrator(db_session_factory=mock_db_factory, permissions=perms)
    # Mock monitor to return None
    orch.monitor = MagicMock(scan=MagicMock(return_value=None))
    result = orch.run_cycle()
    assert result["had_event"] is False
    assert orch.metrics["cycles_total"] == 1

def test_cycle_with_event(mock_db_factory, perms):
    orch = AIOpsOrchestrator(db_session_factory=mock_db_factory, permissions=perms)
    orch.monitor = MagicMock(scan=MagicMock(return_value={"type": "HIGH_CPU", "value": 95}))
    orch.diagnosis.analyze = MagicMock(return_value={"cause": "CPU", "severity": "high", "suggested_action": {"tool": "shell", "args": {"cmd": "top"}}})
    orch.decision.decide = MagicMock(return_value={"action": {"tool": "shell", "args": {"cmd": "top"}}, "auto": False})
    orch.executor.execute = MagicMock(return_value={"status": "success"})
    result = orch.run_cycle()
    assert result["had_event"] is True
    assert orch.metrics["events_detected"] == 1
    assert orch.metrics["diagnoses_made"] == 1
    assert orch.metrics["decisions_total"] == 1
    assert orch.metrics["actions_executed"] == 1
