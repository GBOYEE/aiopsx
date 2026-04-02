import subprocess
from typing import Dict, Any

def ping(host: str, count: int = 4) -> Dict[str, Any]:
    try:
        result = subprocess.run(["ping", "-c", str(count), host], capture_output=True, text=True, timeout=15)
        return {"status": "success" if result.returncode == 0 else "error", "output": result.stdout}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def traceroute(host: str) -> Dict[str, Any]:
    try:
        result = subprocess.run(["traceroute", "-n", host], capture_output=True, text=True, timeout=30)
        return {"status": "success" if result.returncode == 0 else "error", "output": result.stdout}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def check_port(host: str, port: int) -> Dict[str, Any]:
    try:
        import socket
        sock = socket.socket()
        sock.settimeout(5)
        res = sock.connect_ex((host, port))
        sock.close()
        return {"status": "success" if res == 0 else "error", "open": res == 0}
    except Exception as e:
        return {"status": "error", "error": str(e)}
