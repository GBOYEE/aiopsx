import contextvars
from typing import Optional

trace_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar('trace_id', default=None)

def get_trace_id() -> Optional[str]:
    return trace_id_var.get()

def set_trace_id(tid: str):
    trace_id_var.set(tid)
