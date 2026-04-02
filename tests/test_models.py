import pytest
from datetime import datetime
from aiopsx.state.models import Event, Approval, EventType

def test_event_crud(db_session):
    ev = Event(
        event_id="ev1",
        type=EventType.cycle_start,
        payload={"test": 1},
        timestamp=datetime.utcnow(),
        source="orchestrator",
    )
    db_session.add(ev)
    db_session.commit()
    fetched = db_session.query(Event).filter_by(event_id="ev1").first()
    assert fetched is not None
    assert fetched.payload["test"] == 1

def test_approval_crud(db_session):
    appr = Approval(
        approval_id="ap1",
        task_id="cycle1",
        step=1,
        tool="shell",
        args={"cmd": "test"},
        status="pending",
        created_at=datetime.utcnow(),
    )
    db_session.add(appr)
    db_session.commit()
    got = db_session.query(Approval).filter_by(approval_id="ap1").first()
    assert got.tool == "shell"
    assert got.status == "pending"
