# aiopsx — AI Deployment & Monitoring Toolkit

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker&logoColor=white)](https://www.docker.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-✓-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-✓-red?logo=streamlit&logoColor=white)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-✓-blue?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-✓-red?logo=redis&logoColor=white)](https://redis.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 What Problem This Solves

Deploying and monitoring AI agents in production is complex: you need health checks, metrics, logging, rollback on failure, and human approval gates. Most DIY solutions are brittle and lack audit trails. aiopsx provides a complete ops toolkit tailored for AI workloads.

## ⚙️ How It Works

aiopsx wraps your AI agent services with:
- **FastAPI control plane** for health checks, metrics, and actions
- **Streamlit dashboard** for human-in-the-loop approvals
- **PostgreSQL** for persistent state and immutable audit logs
- **Redis** for event bus and coordination
- **Docker Compose** setup with one-command deploy
- **Policy engine** (permissions.yaml) to define auto vs. manual actions

Services report health to `/health` and metrics to `/metrics`. When degradation is detected, the system can auto-rollback or pause for human review via the Streamlit dashboard.

## 📈 Why It Matters

- **Production reliability**: Built-in rollback ensures failures don't cascade
- **Auditability**: Every decision and action is logged with timestamps and user context
- **Speed**: Deploy a new agent service in minutes, not days
- **Control**: Granular permissions define what requires human approval
- **Observability**: Out-of-the-box Prometheus metrics and structured logs

Result: You can run AI agents at scale with confidence.

---

## ✨ Why this exists

Modern infrastructure generates floods of alerts. Manual triage is slow, error‑prone, and lacks auditability. aiopsx turns LLMs into a reliable autonomous infrastructure engineer that monitors, diagnoses, decides, and acts—safely.

## Key Features

- Real-time metrics + LLM-powered diagnosis
- Policy-driven decisions (auto / human-approval / block)
- Safe execution with automatic rollback on degradation
- Full audit trail & Streamlit approval dashboard
- Docker‑Compose ready, tests, CI, permissions.yaml

## Architecture

```mermaid
flowchart TD
    subgraph "Monitoring"
        A[System Metrics] --> B[Alert Engine]
    end
    B --> C{LLM Diagnosis}
    C --> D[Plan Actions]
    D --> E{Policy Gate}
    E -->|Auto| F[Execute Action]
    E -->|Human Approval| G[Approval Dashboard]
    E -->|Block| H[Notify & Log]
    G -->|Approve| F
    G -->|Reject| H
    F --> I[Post‑action Health Check]
    I -->|Degraded| J[Rollback]
    I -->|OK| K[Log Success]
    J --> K
    K --> L[(Postgres Audit)]
    H --> L
```

## Quick Start

```bash
# Clone and run
git clone https://github.com/GBOYEE/aiopsx.git
cd aiopsx
cp .env.example .env
# Edit .env with your LLM API key if needed (Ollama works by default)
docker compose up --build -d
```

Open dashboard: `http://localhost:8501`

## Stack

- **FastAPI** — control plane & webhooks
- **Streamlit** — approval & monitoring dashboard
- **PostgreSQL** — state & audit logs
- **Redis** — event bus & coordination
- **Ollama / OpenAI** — LLM diagnosis
- **Docker Compose** — one‑command deploy

## Safety & Governance

- Human‑in‑the‑loop for high‑risk actions via Streamlit approvals
- Automatic rollback if health degrades after action
- Immutable audit log (who approved, what changed, outcomes)
- Granular permissions via `permissions.yaml`
- Test suite + pre‑commit hooks

## Status

v1.2.0 — Production‑ready, fully tested, CI enabled.

## License

MIT
