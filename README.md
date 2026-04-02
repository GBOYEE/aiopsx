# AIOPS-X 🚀

Autonomous infrastructure AI engineer with controlled autonomy — monitors, diagnoses, and fixes issues with safety and human-in-the-loop oversight.

[![CI](https://github.com/GBOYEE/aiops-x/actions/workflows/ci.yml/badge.svg)](https://github.com/GBOYEE/aiops-x)
[![Coverage](https://codecov.io/gh/GBOYEE/aiops-x/branch/main/graph/badge.svg)](https://codecov.io/gh/GBOYEE/aiops-x)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is AIOPS-X?

AIOPS-X is a production-grade system that:

- **Monitors** system metrics (CPU, memory, disk, services) with configurable thresholds
- **Diagnoses** anomalies using LLMs (local or OpenAI) with structured prompts
- **Decides** actions based on severity and safety policy (auto/approval/block)
- **Executes** approved actions with safe tool wrappers and rollback logic
- **Provides** real-time dashboard and approval UI for human oversight

All actions are logged, auditable, and reversible. Designed for job-ready portfolio demonstration.

---

## Quick Start (Docker Compose)

```bash
git clone https://github.com/GBOYEE/aiops-x
cd aiops-x
cp .env.example .env
# adjust .env if needed (e.g., disable approval for quick test)

docker-compose up -d
# API: http://localhost:8000
# Dashboard: http://localhost:8501 (Streamlit)
```

---

## Architecture

```mermaid
graph TD
    Monitor -->|event| Orchestrator
    Orchestrator --> Diagnosis[Diagnosis Agent]
    Diagnosis -->|diagnosis| Decision[Decision Agent]
    Decision -->|action| Executor[Executor Agent]
    Executor -->|tool| Tools[System Tools]
    Orchestrator -->|audit| DB[(PostgreSQL)]
    Decision -->|if medium/high| Approval[Approval Queue]
    Approval -->|human approves| Executor

    subgraph "AIOPS-X Core"
        Monitor
        Orchestrator
        Diagnosis
        Decision
        Executor
    end
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health |
| `GET` | `/metrics` | Prometheus-style metrics |
| `GET` | `/events` | List recent monitor events |
| `GET` | `/decisions` | List recent AI decisions |
| `POST` | `/run_cycle` | Manually trigger monitor→diagnose→decide |
| `GET` | `/approvals/pending` | List pending actions |
| `POST` | `/approvals/{id}/approve` | Approve an action |
| `POST` | `/approvals/{id}/reject` | Reject an action |

---

## Safety

- **Tool permissions** — risk levels defined in `config/permissions.yaml`
- **Approval workflow** — medium/high actions require human approval
- **Rollback** — executor records state before changes; can revert on failure
- **Audit trail** — all events, decisions, actions stored in PostgreSQL

---

## Dashboard

Streamlit UI (`dashboard/app.py`) provides:

- Live system metrics (CPU, memory, disk)
- Recent events and AI reasoning
- Pending approvals with approve/reject buttons
- Success rate charts

Run: `streamlit run dashboard/app.py`

---

## Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run API
uvicorn api.server:app --reload

# Run tests
pytest tests/ -v --cov=.

# Lint
black . && isort . && flake8 . && mypy .
```

---

## Configuration

Environment variables (`.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `AIOPS_ENV` | `production` | Environment |
| `AIOPS_PORT` | `8000` | API port |
| `DATABASE_URL` | `postgresql+psycopg2://aiopsx:aiopsx@localhost:5432/aiopsx` | PostgreSQL |
| `OLLAMA_URL` | `http://localhost:11434` | Local LLM endpoint |
| `OPENAI_API_KEY` | `` | Optional OpenAI fallback |
| `MONITOR_INTERVAL` | `60` | Seconds between checks |
| `APPROVAL_TIMEOUT` | `3600` | Seconds before approval expires |

Permissions: `config/permissions.yaml`.

---

## License

MIT — see [LICENSE](LICENSE).
