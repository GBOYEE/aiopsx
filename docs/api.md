# aiopsx API Reference

## Control Plane (FastAPI)

- `GET /health` — overall system health
- `GET /metrics` — Prometheus-format metrics
- `GET /agents` — list registered agents
- `POST /actions` — request an action (requires policy approval)
- `GET /pending-approvals` — list items needing human OK

## Dashboard (Streamlit)

Run `streamlit run dashboard/Home.py`. Access at `http://localhost:8501`.

Provides:
- Pending approvals table (approve/reject)
- Agent status grid
- Metrics charts
- Audit log viewer

## Permissions

See `permissions.yaml` for policy definitions: which actions are `auto`, `approval`, or `block`.
