"""Configuration for AIOPS-X."""
import os
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class DatabaseConfig:
    url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///aiopsx.db"))

@dataclass
class MonitorConfig:
    check_interval: int = field(default_factory=lambda: int(os.getenv("MONITOR_INTERVAL", "60")))
    cpu_threshold: int = field(default_factory=lambda: int(os.getenv("CPU_THRESHOLD", "85")))
    memory_threshold: int = field(default_factory=lambda: int(os.getenv("MEMORY_THRESHOLD", "90")))
    disk_threshold: int = field(default_factory=lambda: int(os.getenv("DISK_THRESHOLD", "90")))

@dataclass
class GatewayConfig:
    port: int = field(default_factory=lambda: int(os.getenv("AIOPS_PORT", "8000")))
    secret: str = field(default_factory=lambda: os.getenv("AIOPS_SECRET", "change-me"))

@dataclass
class PermissionsConfig:
    path: str = field(default_factory=lambda: str(Path(__file__).parent.parent / "config" / "permissions.yaml"))

@dataclass
class Settings:
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    monitor: MonitorConfig = field(default_factory=MonitorConfig)
    gateway: GatewayConfig = field(default_factory=GatewayConfig)
    permissions: PermissionsConfig = field(default_factory=PermissionsConfig)
    ENV: str = field(default_factory=lambda: os.getenv("AIOPS_ENV", "production"))

settings = Settings()
