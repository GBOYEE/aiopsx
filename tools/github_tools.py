import os
import requests
from typing import Dict, Any

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API = "https://api.github.com"

def _headers():
    if not GITHUB_TOKEN:
        return {}
    return {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}

def create_issue(owner: str, repo: str, title: str, body: str = "", labels: list = None) -> Dict[str, Any]:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/issues"
    payload = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels
    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {"status": "success", "url": data["html_url"], "number": data["number"]}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def comment_pr(owner: str, repo: str, pr_number: int, body: str) -> Dict[str, Any]:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/issues/{pr_number}/comments"
    payload = {"body": body}
    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {"status": "success", "url": data["html_url"]}
    except Exception as e:
        return {"status": "error", "error": str(e)}
