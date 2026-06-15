import pytest
from fastapi.testclient import TestClient

from main import app
from app.api.parse_routes import get_validated_user
from tests.factories.user import make_valid_user

client = TestClient(app)


def _mock_valid_user():
    return make_valid_user()


@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_validated_user] = _mock_valid_user
    yield
    app.dependency_overrides = {}


class TestParseBudgetSync:
    def test_null_provider_returns_ai_available_false(self):
        response = client.post("/api/v1/ai/parse-budget")
        assert response.status_code == 200
        assert response.json()["ai_available"] is False

    def test_requires_authentication(self):
        app.dependency_overrides = {}
        response = client.post("/api/v1/ai/parse-budget")
        assert response.status_code == 401
        app.dependency_overrides[get_validated_user] = _mock_valid_user


class TestParseBudgetStream:
    def test_null_provider_stream_returns_unavailable_event(self):
        response = client.get("/api/v1/ai/parse-budget/stream?text=test")
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        assert "event: unavailable" in response.text

    def test_rate_limit_header_present_in_response(self):
        response = client.get("/api/v1/ai/parse-budget/stream?text=test")
        assert response.status_code == 200
        assert "x-ratelimit-limit" in response.headers

    def test_requires_authentication(self):
        app.dependency_overrides = {}
        response = client.get("/api/v1/ai/parse-budget/stream?text=test")
        assert response.status_code == 401
        app.dependency_overrides[get_validated_user] = _mock_valid_user
