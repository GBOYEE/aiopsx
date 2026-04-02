"""Monitor Agent — checks system metrics and raises events if thresholds exceeded."""
import os
import psutil
from typing import Dict, Any

class MonitorAgent:
    def __init__(self, cpu_threshold: int = 85, memory_threshold: int = 90, disk_threshold: int = 90):
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold

    def scan(self) -> Dict[str, Any]:
        """Inspect system and return an event dict if a threshold is breached, else None."""
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        if cpu > self.cpu_threshold:
            return {"type": "HIGH_CPU", "value": cpu, "timestamp": psutil.boot_time()}
        if memory > self.memory_threshold:
            return {"type": "HIGH_MEMORY", "value": memory, "timestamp": psutil.boot_time()}
        if disk > self.disk_threshold:
            return {"type": "HIGH_DISK", "value": disk, "timestamp": psutil.boot_time()}
        return None
