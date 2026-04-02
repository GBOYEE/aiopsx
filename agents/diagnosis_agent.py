"""Diagnosis Agent — uses LLM to analyze events and determine root cause."""
import os
import json
import requests
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential

class DiagnosisAgent:
    def __init__(self, ollama_url: str = None, openai_api_key: str = None, model: str = "phi3"):
        self.ollama_url = ollama_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def analyze(self, event: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self._build_prompt(event)
        # Try Ollama first with retry
        try:
            text = self._call_ollama(prompt)
            if text:
                return self._parse_llm_output(text)
        except Exception:
            pass
        # Fallback: deterministic rules
        return self._rule_based_diagnosis(event)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _call_ollama(self, prompt: str) -> str:
        resp = requests.post(f"{self.ollama_url}/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }, timeout=30)
        resp.raise_for_status()
        return resp.json().get("response", "")

    def _build_prompt(self, event: Dict[str, Any]) -> str:
        return f"""
Analyze this system event and provide JSON with:
- cause: short string
- severity: low|medium|high
- suggested_action: recommended tool and args

Event: {json.dumps(event)}

Output JSON only:
"""

    def _parse_llm_output(self, text: str) -> Dict[str, Any]:
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
        return {"cause": "unknown", "severity": "medium", "suggested_action": {"tool": "shell", "args": {"cmd": "echo diagnosis failed"}}}

    def _rule_based_diagnosis(self, event: Dict[str, Any]) -> Dict[str, Any]:
        t = event.get("type")
        if t == "HIGH_CPU":
            return {"cause": "CPU overload", "severity": "high", "suggested_action": {"tool": "shell", "args": {"cmd": "ps aux --sort=-%cpu | head -10"}}}
        if t == "HIGH_MEMORY":
            return {"cause": "Memory pressure", "severity": "high", "suggested_action": {"tool": "shell", "args": {"cmd": "ps aux --sort=-%mem | head -10"}}}
        if t == "HIGH_DISK":
            return {"cause": "Disk full", "severity": "high", "suggested_action": {"tool": "disk_clean", "args": {"limit_mb": 1000}}}
        return {"cause": "unknown", "severity": "medium", "suggested_action": {"tool": "shell", "args": {"cmd": "echo no diagnosis"}}}
