"""Model router — selects appropriate model based on task type."""
import os

def route_task(task_type: str) -> str:
    """Return model name for given task type."""
    mapping = {
        "analysis": os.getenv("MODEL_ANALYSIS", "phi3"),
        "reasoning": os.getenv("MODEL_REASONING", "qwen"),
        "default": os.getenv("MODEL_DEFAULT", "llama3"),
    }
    return mapping.get(task_type, mapping["default"])
