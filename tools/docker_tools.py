import subprocess
from typing import Dict, Any

def docker_ps() -> Dict[str, Any]:
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}\\t{{.Status}}"], capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split("\\n") if result.stdout else []
        containers = []
        for line in lines:
            if "\\t" in line:
                name, status = line.split("\\t", 1)
                containers.append({"name": name, "status": status})
        return {"status": "success", "containers": containers}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def restart_container(container: str) -> Dict[str, Any]:
    try:
        result = subprocess.run(["docker", "restart", container], capture_output=True, text=True, timeout=30)
        return {"status": "success" if result.returncode == 0 else "error", "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def stop_container(container: str) -> Dict[str, Any]:
    try:
        result = subprocess.run(["docker", "stop", container], capture_output=True, text=True, timeout=30)
        return {"status": "success" if result.returncode == 0 else "error", "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}
