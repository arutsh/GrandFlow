import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# from app.api.budget_routes import router
from main import app  # Make sure your FastAPI app includes the router

# If your app is not available, you can create a test app:
# from fastapi import FastAPI
# app = FastAPI()
# app.include_router(router)

client = TestClient(app)


@pytest.fixture
def auth_headers():
    # Simulate authentication header
    return {"Authorization": "Bearer testtoken"}


def test_create_budget_endpoint(auth_headers):
    payload = {
        "name": "Test Budget",
        "owner_id": "ngo123",
        "funding_customer_id": "donor456",
        "external_funder_name": "name123",
    }
    # Patch create_budget to avoid DB calls
    with patch("app.crud.budget_crud.create_budget") as mock_create, patch(
        "app.utils.security.get_current_user", return_value={"user_id": "user789"}
    ):
        mock_create.return_value = MagicMock(
            id=1,
            name="Test Budget",
            owner_id="ngo123",
            funding_customer_id="donor456",
            external_funder_name="name123",
        )
        response = client.post("/budgets/", json=payload, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["status"] == "created"
        assert response.json()["budget"]["name"] == "Test Budget"


def test_get_budget_endpoint_found(auth_headers):
    with patch("app.crud.budget_crud.get_budget") as mock_get, patch(
        "app.utils.security.get_current_user", return_value={"user_id": "user789"}
    ):
        mock_get.return_value = {
            "id": 1,
            "name": "Test Budget",
            "ngo_id": "ngo123",
            "donor_id": "donor456",
        }
        response = client.get("/budgets/1", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Test Budget"


def test_get_budget_endpoint_not_found(auth_headers):
    with patch("app.crud.budget_crud.get_budget") as mock_get, patch(
        "app.utils.security.get_current_user", return_value={"user_id": "user789"}
    ):
        mock_get.return_value = None
        response = client.get("/budgets/999", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["error"] == "Budget not found"


def test_update_budget_endpoint(auth_headers):
    payload = {
        "name": "Updated Budget",
        "ngo_id": "ngo123",
        "donor_id": "donor456",
        "confidence": 0.95,
    }
    with patch("app.crud.budget_crud.update_budget") as mock_update, patch(
        "app.utils.security.get_current_user", return_value={"user_id": "user789"}
    ):
        mock_update.return_value = {
            "id": 1,
            "name": "Updated Budget",
            "ngo_id": "ngo123",
            "donor_id": "donor456",
        }
        response = client.put("/budgets/1", json=payload, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Budget"


def test_get_budgets(auth_headers):
    with patch("app.crud.budget_crud.list_budgets") as mock_list, patch(
        "app.utils.security.get_current_user", return_value={"user_id": "user789"}
    ):
        mock_list.return_value = [
            {"id": 1, "name": "Budget1", "ngo_id": "ngo123", "donor_id": "donor456"},
            {"id": 2, "name": "Budget2", "ngo_id": "ngo124", "donor_id": "donor457"},
        ]
        response = client.get("/budgets/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2
