"""SQLAlchemy models for AIOPS-X."""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import enum

Base = declarative_base()

class EventType(str, enum.Enum):
    cycle_start = "cycle_start"
    event_detected = "event_detected"
    diagnosis = "diagnosis"
    decision = "decision"
    execution = "execution"
    cycle_complete = "cycle_complete"
    approval_requested = "approval_requested"
    approval_granted = "approval_granted"
    approval_rejected = "approval_rejected"

class Event(Base):
    __tablename__ = "events"
    event_id = Column(String, primary_key=True)
    type = Column(SQLEnum(EventType), nullable=False)
    task_id = Column(String, nullable=True, index=True)  # cycle_id
    payload = Column(JSON, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    source = Column(String, nullable=True)

class Approval(Base):
    __tablename__ = "approvals"
    approval_id = Column(String, primary_key=True)
    task_id = Column(String, nullable=False, index=True)  # cycle_id
    step = Column(Integer, nullable=False)  # typically 1
    tool = Column(String, nullable=False)
    args = Column(JSON, nullable=False)
    requested_by = Column(String, nullable=True, default="system")
    status = Column(String, nullable=False, default="pending")
    granted_by = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    decided_at = Column(DateTime, nullable=True)

def init_db(database_url: str):
    engine = create_engine(database_url, echo=False, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session
