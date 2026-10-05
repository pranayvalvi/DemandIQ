import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'app'))
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_inventory_logic_negative_stock():
    # Test that the API safely handles inventory scenarios
    payload = {
        "store": "Store_A",
        "product": "Apples",
        "category": "Produce",
        "forecast_date": "2026-10-15",
        "price": 5.0,
        "promotion": 0,
        "holiday": 0,
        "inventory": 0,
        "lag_1": 30,
        "lag_7": 30,
        "lag_14": 30,
        "lag_28": 30,
        "rolling_mean_7": 30.0,
        "rolling_mean_14": 30.0,
        "rolling_mean_28": 30.0
    }
    response = client.post("/api/inventory-insights", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["stock_status"] == "LOW STOCK"
    assert data["expected_shortage"] > 0
    assert "safety_stock" in data
