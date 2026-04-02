"""AIOPS-X Orchestrator — runs monitor → diagnose → decide → execute cycle."""
import time
import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from ..state.models import Event, init_db, EventType
from ..telemetry import get_trace_id

logger = logging.getLogger("aiopsx.orchestrator")

class AIOpsOrchestrator:
    def __init__(self, db_session_factory, permissions: Dict[str, Any], monitor_interval: int = 60):
        self.db = db_session_factory
        self.perms = permissions
        self.monitor_interval = monitor_interval
        self.metrics = {
            "cycles_total": 0,
            "events_detected": 0,
            "diagnoses_made": 0,
            "decisions_total": 0,
            "actions_executed": 0,
            "approvals_requested": 0,
        }
        # Agents
        from ..agents.monitor_agent import MonitorAgent
        from ..agents.diagnosis_agent import DiagnosisAgent
        from ..agents.decision_agent import DecisionAgent
        from ..agents.executor_agent import ExecutorAgent
        self.monitor = MonitorAgent()
        self.diagnosis = DiagnosisAgent()
        self.decision = DecisionAgent(permissions)
        self.executor = ExecutorAgent(db_session_factory, permissions)

    def run_cycle(self) -> Dict[str, Any]:
        """Runs one full cycle and returns a summary."""
        cycle_id = str(uuid.uuid4())
        start = time.time()
        self._log_event(cycle_id, "cycle_start", {})
        result = {"cycle_id": cycle_id, "events": []}

        # 1. Monitor
        event = self.monitor.scan()
        if not event:
            self._log_event(cycle_id, "cycle_complete", {"had_event": False})
            result["had_event"] = False
            result["duration_s"] = time.time() - start
            self.metrics["cycles_total"] += 1
            return result

        self.metrics["events_detected"] += 1
        self._log_event(cycle_id, "event_detected", event)
        result["events"].append(event)

        # 2. Diagnose
        diagnosis = self.diagnosis.analyze(event)
        self.metrics["diagnoses_made"] += 1
        self._log_event(cycle_id, "diagnosis", diagnosis)
        result["diagnosis"] = diagnosis

        # 3. Decide
        decision = self.decision.decide(diagnosis)
        self.metrics["decisions_total"] += 1
        self._log_event(cycle_id, "decision", decision)
        result["decision"] = decision

        # 4. Execute (if action present)
        if decision.get("action"):
            exec_result = self.executor.execute(decision, cycle_id)
            self.metrics["actions_executed"] += 1
            self._log_event(cycle_id, "execution", exec_result)
            result["execution"] = exec_result
        else:
            result["execution"] = None

        result["had_event"] = True
        result["duration_s"] = time.time() - start
        self._log_event(cycle_id, "cycle_complete", {"had_event": True})
        self.metrics["cycles_total"] += 1
        return result

    def _log_event(self, cycle_id: str, type_: str, payload: Dict[str, Any]):
        # Inject trace_id into payload for correlation
        payload_with_trace = dict(payload)
        trace_id = get_trace_id()
        if trace_id:
            payload_with_trace['trace_id'] = trace_id
        with self.db() as session:
            ev = Event(
                event_id=str(uuid.uuid4()),
                type=EventType(type_),
                task_id=cycle_id,
                payload=payload_with_trace,
                timestamp=datetime.utcnow(),
                source="orchestrator",
            )
            session.add(ev)
            session.commit()
        logger.info("Event", extra={"cycle_id": cycle_id, "type": type_, "trace_id": trace_id})
