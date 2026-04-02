import pytest
from aiopsx.agents.monitor_agent import MonitorAgent

def test_monitor_high_cpu(monkeypatch):
    class MockCPU:
        @staticmethod
        def cpu_percent(interval=None):
            return 90.0
        @staticmethod
        def virtual_memory():
            class Mem:
                percent = 50
            return Mem()
        @staticmethod
        def disk_usage(path):
            class Disk:
                percent = 30
            return Disk()
        @staticmethod
        def boot_time():
            return 12345
    monkeypatch.setattr("psutil.cpu_percent", MockCPU.cpu_percent)
    monkeypatch.setattr("psutil.virtual_memory", MockCPU.virtual_memory)
    monkeypatch.setattr("psutil.disk_usage", MockCPU.disk_usage)
    monkeypatch.setattr("psutil.boot_time", MockCPU.boot_time)
    mon = MonitorAgent(cpu_threshold=85)
    event = mon.scan()
    assert event is not None
    assert event["type"] == "HIGH_CPU"
    assert event["value"] == 90.0

def test_monitor_high_memory(monkeypatch):
    class MockMem:
        @staticmethod
        def cpu_percent(interval=None):
            return 10.0
        @staticmethod
        def virtual_memory():
            class Mem:
                percent = 95
            return Mem()
        @staticmethod
        def disk_usage(path):
            class Disk:
                percent = 20
            return Disk()
        @staticmethod
        def boot_time():
            return 12345
    monkeypatch.setattr("psutil.cpu_percent", MockMem.cpu_percent)
    monkeypatch.setattr("psutil.virtual_memory", MockMem.virtual_memory)
    monkeypatch.setattr("psutil.disk_usage", MockMem.disk_usage)
    monkeypatch.setattr("psutil.boot_time", MockMem.boot_time)
    mon = MonitorAgent(memory_threshold=90)
    event = mon.scan()
    assert event is not None
    assert event["type"] == "HIGH_MEMORY"

def test_monitor_ok(monkeypatch):
    class MockOk:
        @staticmethod
        def cpu_percent(interval=None):
            return 10.0
        @staticmethod
        def virtual_memory():
            class Mem:
                percent = 30
            return Mem()
        @staticmethod
        def disk_usage(path):
            class Disk:
                percent = 40
            return Disk()
        @staticmethod
        def boot_time():
            return 12345
    monkeypatch.setattr("psutil.cpu_percent", MockOk.cpu_percent)
    monkeypatch.setattr("psutil.virtual_memory", MockOk.virtual_memory)
    monkeypatch.setattr("psutil.disk_usage", MockOk.disk_usage)
    monkeypatch.setattr("psutil.boot_time", MockOk.boot_time)
    mon = MonitorAgent()
    event = mon.scan()
    assert event is None
