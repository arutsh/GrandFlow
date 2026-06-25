from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from main import app
from app.api.settings_routes import get_db, get_validated_user
from tests.factories.user import make_valid_user

client = TestClient(app)

_ENCRYPTED_KEY = "dGVzdC1lbmNyeXB0ZWQ="  # fake base64 blob

_LIST_ACTIVE = "app.api.settings_routes.list_active"
_GET_KEY = "app.api.settings_routes.get_key"
_GET_BY_NAME = "app.api.settings_routes.get_by_name"
_VALIDATE = "app.api.settings_routes._validate_key_with_provider"
_ENCRYPT = "app.api.settings_routes.encrypt"
_UPSERT = "app.api.settings_routes.upsert_key"
_DELETE = "app.api.settings_routes.delete_key"


def _make_admin_user():
    return make_valid_user(role="superuser")


def _make_regular_user():
    return make_valid_user(role="user")


def _make_provider(name="anthropic", has_key_prefix=True):
    p = MagicMock()
    p.id = "bbbbbbbb-0000-0000-0000-000000000002"
    p.name = name
    p.display_name = "Anthropic" if name == "anthropic" else "Ollama (Local)"
    p.key_prefix = "sk-ant-" if has_key_prefix else None
    p.is_active = True
    return p


def _make_key_row(has_key: bool):
    if not has_key:
        return None
    row = MagicMock()
    row.encrypted_key = _ENCRYPTED_KEY
    row.model_name = "claude-sonnet-4-6"
    row.base_url = None
    return row


def _mock_db():
    async def _override():
        yield AsyncMock()

    return _override


class TestGetAiSettings:
    def setup_method(self):
        app.dependency_overrides[get_validated_user] = _make_admin_user
        app.dependency_overrides[get_db] = _mock_db()

    def teardown_method(self):
        app.dependency_overrides.pop(get_validated_user, None)
        app.dependency_overrides.pop(get_db, None)

    def test_returns_providers_list_with_has_key_true(self):
        with (
            patch(_LIST_ACTIVE, new=AsyncMock(return_value=[_make_provider()])),
            patch(_GET_KEY, new=AsyncMock(return_value=_make_key_row(has_key=True))),
        ):
            response = client.get("/api/v1/ai/settings")
        assert response.status_code == 200
        data = response.json()
        assert len(data["providers"]) == 1
        p = data["providers"][0]
        assert p["name"] == "anthropic"
        assert p["has_key"] is True
        assert p["requires_key"] is True
        assert p["model"] == "claude-sonnet-4-6"

    def test_returns_has_key_false_when_no_key(self):
        with (
            patch(_LIST_ACTIVE, new=AsyncMock(return_value=[_make_provider()])),
            patch(_GET_KEY, new=AsyncMock(return_value=None)),
        ):
            response = client.get("/api/v1/ai/settings")
        assert response.status_code == 200
        assert response.json()["providers"][0]["has_key"] is False

    def test_ollama_provider_requires_no_key(self):
        with (
            patch(
                _LIST_ACTIVE,
                new=AsyncMock(
                    return_value=[_make_provider("ollama", has_key_prefix=False)]
                ),
            ),
            patch(_GET_KEY, new=AsyncMock(return_value=None)),
        ):
            response = client.get("/api/v1/ai/settings")
        p = response.json()["providers"][0]
        assert p["requires_key"] is False

    def test_user_role_forbidden(self):
        app.dependency_overrides[get_validated_user] = _make_regular_user
        response = client.get("/api/v1/ai/settings")
        assert response.status_code == 403


class TestSaveAiSettings:
    def setup_method(self):
        app.dependency_overrides[get_validated_user] = _make_admin_user
        app.dependency_overrides[get_db] = _mock_db()

    def teardown_method(self):
        app.dependency_overrides.pop(get_validated_user, None)
        app.dependency_overrides.pop(get_db, None)

    def test_unknown_provider_returns_404(self):
        with patch(_GET_BY_NAME, new=AsyncMock(return_value=None)):
            response = client.put(
                "/api/v1/ai/settings",
                json={"provider": "unknown", "key": "any", "model": "claude-sonnet-4-6"},
            )
        assert response.status_code == 404

    def test_invalid_key_format_rejected(self):
        with patch(_GET_BY_NAME, new=AsyncMock(return_value=_make_provider())):
            response = client.put(
                "/api/v1/ai/settings",
                json={
                    "provider": "anthropic",
                    "key": "not-a-valid-key",
                    "model": "claude-sonnet-4-6",
                },
            )
        assert response.status_code == 422

    def test_unsupported_model_rejected(self):
        response = client.put(
            "/api/v1/ai/settings",
            json={"provider": "anthropic", "key": "sk-ant-x", "model": "gpt-5-turbo"},
        )
        assert response.status_code == 422

    def test_valid_key_saved_returns_providers(self):
        with (
            patch(_GET_BY_NAME, new=AsyncMock(return_value=_make_provider())),
            patch(_VALIDATE, new=AsyncMock()),
            patch(_ENCRYPT, return_value=_ENCRYPTED_KEY),
            patch(_UPSERT, new=AsyncMock()),
            patch(_LIST_ACTIVE, new=AsyncMock(return_value=[_make_provider()])),
            patch(_GET_KEY, new=AsyncMock(return_value=_make_key_row(has_key=True))),
        ):
            response = client.put(
                "/api/v1/ai/settings",
                json={
                    "provider": "anthropic",
                    "key": "sk-ant-api03-x",
                    "model": "claude-sonnet-4-6",
                },
            )
        assert response.status_code == 200
        assert response.json()["providers"][0]["has_key"] is True

    def test_user_role_forbidden(self):
        app.dependency_overrides[get_validated_user] = _make_regular_user
        response = client.put(
            "/api/v1/ai/settings",
            json={"provider": "anthropic", "key": "sk-ant-api03-x", "model": "claude-sonnet-4-6"},
        )
        assert response.status_code == 403


class TestClearAiKey:
    def setup_method(self):
        app.dependency_overrides[get_validated_user] = _make_admin_user
        app.dependency_overrides[get_db] = _mock_db()

    def teardown_method(self):
        app.dependency_overrides.pop(get_validated_user, None)
        app.dependency_overrides.pop(get_db, None)

    def test_unknown_provider_returns_404(self):
        with patch(_GET_BY_NAME, new=AsyncMock(return_value=None)):
            response = client.delete("/api/v1/ai/settings/unknown/key")
        assert response.status_code == 404

    def test_clears_key_returns_has_key_false(self):
        with (
            patch(_GET_BY_NAME, new=AsyncMock(return_value=_make_provider())),
            patch(_DELETE, new=AsyncMock()),
            patch(_LIST_ACTIVE, new=AsyncMock(return_value=[_make_provider()])),
            patch(_GET_KEY, new=AsyncMock(return_value=None)),
        ):
            response = client.delete("/api/v1/ai/settings/anthropic/key")
        assert response.status_code == 200
        assert response.json()["providers"][0]["has_key"] is False

    def test_user_role_forbidden(self):
        app.dependency_overrides[get_validated_user] = _make_regular_user
        response = client.delete("/api/v1/ai/settings/anthropic/key")
        assert response.status_code == 403
