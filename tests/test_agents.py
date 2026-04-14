"""test_agents.py — Unit tests for agent pipeline"""
import pytest
from unittest.mock import patch, MagicMock

def test_api_health(client):
    from fastapi.testclient import TestClient
    from app.api import app
    tc = TestClient(app)
    response = tc.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_property_request_validation():
    from app.api import PropertyRequest
    req = PropertyRequest(address="123 Main St", property_type="SFR",
                          bedrooms=3, bathrooms=2.0, sqft=1500,
                          year_built=2000, asking_price=400000)
    assert req.bedrooms == 3
    assert req.asking_price == 400000

def test_budget_exceeded():
    from utils.cost_tracker import TokenBudget, BudgetExceededError
    budget = TokenBudget(max_tokens=1, model="gpt-4o")
    with pytest.raises(BudgetExceededError):
        budget.add("This text is longer than one token by quite a lot")
