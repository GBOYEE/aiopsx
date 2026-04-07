# aiopsx Architecture

## Components

- **control-plane (FastAPI)**: health checks, metrics, actions
- **dashboard (Streamlit)**: human approvals, monitoring UI
- **postgres**: audit logs, state persistence
- **redis**: event bus, coordination
- **agent services**: your AI agents (could be any framework)

## How It Works

1. Agent services register with control plane
2. Control plane polls health endpoints (`/health`) and scrapes metrics (`/metrics`)
3. On degradation, LLM diagnosis decides action
4. Policy engine (permissions.yaml) determines: auto-execute or human approval
5. If approval needed, Streamlit dashboard shows pending action
6. Upon execution, post-action health check; if degraded, auto-rollback

## Deployment

```bash
docker compose up -d
# Dashboard: http://localhost:8501
# Control plane: http://localhost:8000
```

## Extending

- Write new agent services that implement `/health` and `/metrics`
- Add custom policies in `permissions.yaml`
- Create custom Streamlit pages in `dashboard/`
