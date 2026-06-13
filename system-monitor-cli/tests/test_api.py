import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_metrics_endpoint_empty(monkeypatch):
    """
    Verifica que el endpoint GET /metrics responda correctamente (200 OK)
    cuando no hay registros de logs (retorna lista vacía).
    """
    monkeypatch.setattr("api.read_logs", lambda: [])
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json() == []

def test_metrics_endpoint_with_data(monkeypatch):
    """
    Verifica que el endpoint GET /metrics retorne el listado de logs mockeados.
    """
    mock_logs = [
        {
            "timestamp": "2026-06-13T10:00:00",
            "cpu": 12.5,
            "ram": 60.1,
            "disk": 35.0,
            "network": {
                "bytes_sent": 1000,
                "bytes_recv": 2000
            },
            "top_processes": []
        }
    ]
    monkeypatch.setattr("api.read_logs", lambda: mock_logs)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json() == mock_logs
