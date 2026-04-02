"""System tools with sandboxing."""
import subprocess
import os
from pathlib import Path
from typing import Dict, Any

ALLOWED_SHELL_COMMANDS = {
    "echo", "ls", "cat", "pwd", "whoami", "date",
    "systemctl", "service", "journalctl", "tail", "grep",
    "df", "du", "free", "ps", "top", "kill",
}

def run_shell(cmd: str, capture_output: bool = True, timeout: int = 10) -> Dict[str, Any]:
    first_word = cmd.strip().split()[0] if cmd.strip() else ""
    if first_word not in ALLOWED_SHELL_COMMANDS:
        return {"status": "error", "error": f"Command '{first_word}' not allowed"}
    workspace = Path(os.getenv("AIOPS_WORKSPACE", "/root/.openclaw/workspace"))
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=capture_output, text=True,
            timeout=timeout, cwd=str(workspace),
            env={**os.environ, "PATH": "/usr/bin:/bin:/usr/sbin:/sbin"}
        )
        return {
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout if capture_output else "",
            "stderr": result.stderr if capture_output else "",
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "timeout"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def disk_clean(limit_mb: int = 500) -> Dict[str, Any]:
    """Placeholder: dry-run only for safety."""
    return {"status": "success", "freed_mb": 0, "note": "dry-run; real cleanup not implemented"}

def restart_service(service_name: str) -> Dict[str, Any]:
    allowed = os.getenv("AIOPS_ALLOWED_SERVICES", "").split(",")
    if service_name not in allowed:
        return {"status": "error", "error": f"Service '{service_name}' not whitelisted"}
    try:
        result = subprocess.run(["systemctl", "restart", service_name], capture_output=True, text=True, timeout=30)
        return {"status": "success" if result.returncode == 0 else "error", "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}
