import pytest
from unittest.mock import MagicMock
from aiopsx.agents.executor_agent import ExecutorAgent

def test_execute_shell_success(monkeypatch):
    def fake_run_shell(cmd, **kwargs):
        return {"status": "success", "stdout": "hi"}
    monkeypatch.setattr("aiopsx.tools.system_tools.run_shell", fake_run_shell)
    db_factory = MagicMock()
    perms = {}
    exec = ExecutorAgent(db_factory, perms)
    decision = {"action": {"tool": "shell", "args": {"cmd": "echo hello"}}}
    result = exec.execute(decision, "cycle1")
    assert result["status"] == "success"

def test_execute_unknown_tool():
    db_factory = MagicMock()
    perms = {}
    exec = ExecutorAgent(db_factory, perms)
    decision = {"action": {"tool": "unknown", "args": {}}}
    result = exec.execute(decision, "cycle1")
    assert result["status"] == "error"
    assert "Unknown tool" in result["error"]

def test_executor_no_action():
    db_factory = MagicMock()
    perms = {}
    exec = ExecutorAgent(db_factory, perms)
    decision = {"action": None}
    result = exec.execute(decision, "cycle1")
    assert result["status"] == "no_action"
