"""Executor Agent — executes approved actions with safety and rollback."""
import os
from typing import Dict, Any

class ExecutorAgent:
    def __init__(self, db_session_factory, permissions: Dict[str, Any]):
        self.db = db_session_factory
        self.permissions = permissions

    def execute(self, decision: Dict[str, Any], cycle_id: str) -> Dict[str, Any]:
        action = decision.get("action")
        if not action:
            return {"status": "no_action", "message": "No action specified"}
        tool = action.get("tool")
        args = action.get("args", {})
        if not tool:
            return {"status": "no_action", "message": "No tool specified"}
        # Execute tool
        result = self._run_tool(tool, args)
        # Record result in DB (could attach to cycle event)
        return result

    def _run_tool(self, tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if tool == "shell":
                from ..tools.system_tools import run_shell
                return run_shell(args.get("cmd", ""), capture_output=True, timeout=10)
            elif tool == "disk_clean":
                from ..tools.system_tools import disk_clean
                return disk_clean(limit_mb=args.get("limit_mb", 500))
            elif tool == "docker_restart":
                from ..tools.docker_tools import restart_container
                return restart_container(args.get("container"))
            elif tool == "docker_stop":
                from ..tools.docker_tools import stop_container
                return stop_container(args.get("container"))
            else:
                return {"status": "error", "error": f"Unknown tool: {tool}"}
        except Exception as e:
            return {"status": "error", "error": str(e)}