"""FastAPI server for AIOPS-X with security."""
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
import yaml

from ..state.models import init_db, Event, Approval, EventType
from ..core.orchestrator import AIOpsOrchestrator
from ..config.settings import Settings
from ..telemetry import set_trace_id

app = FastAPI(title="AIOPS-X", version="1.0.0")

# Settings & DB
settings = Settings()
db_factory = init_db(settings.database.url)

# Load permissions
with open(settings.permissions.path) as f:
    PERMISSIONS = yaml.safe_load(f)

# Orchestrator
orchestrator = AIOpsOrchestrator(
    db_session_factory=db_factory,
    permissions=PERMISSIONS,
    monitor_interval=settings.monitor.check_interval
)

# Metrics
metrics = {
    "requests_total": 0,
    "cycles_started": 0,
    "events_detected": orchestrator.metrics["events_detected"],
}

# ----- Auth helpers -----
def verify_api_key(Authorization: Optional[str] = Header(None)):
    api_key = os.getenv("AIOPS_API_KEY")
    if api_key:
        if not Authorization:
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        try:
            scheme, token = Authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid scheme")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid Authorization header")
        if token != api_key:
            raise HTTPException(status_code=401, detail="Invalid API key")

def get_user_role(x_user_id: str) -> str:
    admins = os.getenv("AIOPS_ADMIN_USERS", "").split(",")
    operators = os.getenv("AIOPS_OPERATORS", "").split(",")
    if x_user_id in admins:
        return "admin"
    if x_user_id in operators:
        return "operator"
    return "viewer"

def require_user_id(x_user_id: str = Header(..., alias="X-User-ID")):
    return x_user_id

# ----- Middleware -----
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id
    set_trace_id(request_id)
    start = datetime.utcnow()
    metrics["requests_total"] += 1
    try:
        response = await call_next(request)
        elapsed = (datetime.utcnow() - start).total_seconds() * 1000
        return response
    except Exception as exc:
        metrics["requests_failed"] = metrics.get("requests_failed", 0) + 1
        raise

# ----- Public -----
@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat(), "version": "1.0.0", "environment": settings.ENV}

@app.get("/metrics")
async def get_metrics():
    metrics.update(orchestrator.metrics)
    return metrics

# ----- Protected -----
@app.post("/run_cycle", dependencies=[Depends(verify_api_key)])
async def run_cycle():
    metrics["cycles_started"] += 1
    result = orchestrator.run_cycle()
    return result

@app.get("/events", dependencies=[Depends(verify_api_key)])
async def list_events(limit: int = 50):
    db = db_factory()
    events = db.query(Event).order_by(Event.timestamp.desc()).limit(limit).all()
    return [
        {
            "event_id": e.event_id,
            "type": e.type.value,
            "payload": e.payload,
            "timestamp": e.timestamp.isoformat(),
            "source": e.source,
        }
        for e in events
    ]

# Approvals with role checks
@app.get("/approvals/pending", dependencies=[Depends(verify_api_key)])
def list_pending(db = Depends(lambda: db_factory())):
    approvals = db.query(Approval).filter(Approval.status == "pending").all()
    return [
        {
            "approval_id": a.approval_id,
            "task_id": a.task_id,
            "tool": a.tool,
            "args": a.args,
            "requested_by": a.requested_by,
            "created_at": a.created_at.isoformat(),
        }
        for a in approvals
    ]

@app.post("/approvals/{approval_id}/approve")
def approve(
    approval_id: str,
    request: Request,
    db = Depends(lambda: db_factory()),
    x_user_id: str = Depends(require_user_id),
):
    # Verify API key also via dependency above
    # Role check
    user_role = get_user_role(x_user_id)
    approval = db.query(Approval).filter(Approval.approval_id == approval_id).first()
    if not approval or approval.status != "pending":
        raise HTTPException(status_code=404, detail="Approval not found")
    allowed_roles = PERMISSIONS.get("tools", {}).get(approval.tool, {}).get("allowed_roles", [])
    if user_role not in allowed_roles:
        raise HTTPException(status_code=403, detail=f"User role {user_role} not allowed for tool {approval.tool}")
    approval.status = "granted"
    approval.granted_by = x_user_id
    approval.decided_at = datetime.utcnow()
    db.commit()
    ev = Event(
        event_id=str(uuid.uuid4()),
        type=EventType.approval_granted,
        task_id=approval.task_id,
        payload={"approval_id": approval_id, "tool": approval.tool},
        timestamp=datetime.utcnow(),
        source="api",
    )
    db.add(ev)
    db.commit()
    return {"status": "ok"}

@app.post("/approvals/{approval_id}/reject")
def reject(
    approval_id: str,
    request: Request,
    db = Depends(lambda: db_factory()),
    x_user_id: str = Depends(require_user_id),
):
    user_role = get_user_role(x_user_id)
    approval = db.query(Approval).filter(Approval.approval_id == approval_id).first()
    if not approval or approval.status != "pending":
        raise HTTPException(status_code=404, detail="Approval not found")
    allowed_roles = PERMISSIONS.get("tools", {}).get(approval.tool, {}).get("allowed_roles", [])
    if user_role not in allowed_roles:
        raise HTTPException(status_code=403, detail=f"User role {user_role} not allowed for tool {approval.tool}")
    approval.status = "rejected"
    approval.granted_by = x_user_id
    approval.decided_at = datetime.utcnow()
    db.commit()
    ev = Event(
        event_id=str(uuid.uuid4()),
        type=EventType.approval_rejected,
        task_id=approval.task_id,
        payload={"approval_id": approval_id},
        timestamp=datetime.utcnow(),
        source="api",
    )
    db.add(ev)
    db.commit()
    return {"status": "ok"}
