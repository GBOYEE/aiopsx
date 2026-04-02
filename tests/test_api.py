import pytest
from fastapi.testclient import TestClient
from aiopsx.api.server import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"

def test_metrics(client):
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)
