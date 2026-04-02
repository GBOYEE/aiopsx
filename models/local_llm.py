"""Local LLM client (Ollama)."""
import requests
from typing import Dict, Any

class LocalLLM:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def generate(self, prompt: str, model: str = "phi3", stream: bool = False) -> str:
        resp = requests.post(f"{self.base_url}/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": stream
        }, timeout=60)
        resp.raise_for_status()
        return resp.json().get("response", "")
