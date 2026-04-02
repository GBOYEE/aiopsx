import pytest
from aiopsx.tools.system_tools import run_shell, disk_clean
from aiopsx.tools.docker_tools import docker_ps

def test_run_shell_allowed():
    res = run_shell("echo test", capture_output=True)
    assert res["status"] == "success"
    assert "test" in res.get("stdout", "")

def test_run_shell_not_allowed():
    res = run_shell("rm -rf /", capture_output=False)
    assert res["status"] == "error"
    assert "not allowed" in res["error"]

def test_disk_clean():
    res = disk_clean()
    assert res["status"] == "success"
    assert "dry-run" in res["note"].lower()

def test_docker_ps():
    res = docker_ps()
    assert "status" in res
    # if docker running, expect success; else error
    if res["status"] == "success":
        assert "containers" in res
