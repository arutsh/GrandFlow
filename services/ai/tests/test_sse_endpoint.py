import json
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from main import app
from app.api.parse_routes import get_validated_user
from app.services.prompt_loader import LoadedPrompt
from tests.factories.user import make_valid_user


MOCK_PROMPT = LoadedPrompt(
    name="parse_budget",
    version="v1",
    system_prompt="You are a structured extractor.",
    user_template="{{ text }}",
)

VALID_JSON_RESPONSE = json.dumps(
    {
        "budget_name": "Staff Grant",
        "external_funder_name": "City Foundation",
        "duration_months": 12,
        "lines": [
            {
                "category_name": "Personnel",
                "description": "Program coordinator",
                "amount": 50000.0,
                "extra_fields": None,
            }
        ],
        "ai_available": True,
        "prompt_version": "v1",
    }
)

_LOAD_PROMPT = "app.services.parse_service.load_prompt"
_AUDIT = "app.services.parse_service.write_audit_log"
_RATE = "app.api.parse_routes.check_and_increment"
_RESOLVE = "app.api.parse_routes.resolve_provider"
_GET_SETTINGS = "app.api.parse_routes.get_settings"


def _setup(customer_id="sse-test-customer"):
    app.dependency_overrides[get_validated_user] = (
        lambda: make_valid_user(customer_id=customer_id)
    )
    return TestClient(app)


def _teardown():
    app.dependency_overrides = {}


def _mock_provider(tokens: list[str]):
    """Returns a provider mock whose .stream() coroutine yields the given tokens."""

    async def _gen():
        for t in tokens:
            yield t

    async def _stream(prompt, system_prompt=""):
        return _gen()

    mock = AsyncMock()
    mock.provider_name = "ollama"
    mock.model_name = "llama3.2"
    mock.stream = _stream
    return mock


class TestSSEEndpoint:
    def setup_method(self):
        self.client = _setup()

    def teardown_method(self):
        _teardown()

    def test_response_content_type_is_event_stream(self):
        with (
            patch(_LOAD_PROMPT, new=AsyncMock(return_value=MOCK_PROMPT)),
            patch(_RESOLVE, return_value=_mock_provider([VALID_JSON_RESPONSE])),
            patch(_AUDIT, new=AsyncMock()),
            patch(_RATE, new=AsyncMock(return_value=(True, 0))),
            patch(_GET_SETTINGS, new=AsyncMock(return_value=None)),
        ):
            response = self.client.get("/api/v1/ai/parse-budget/stream?text=test")

        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

    def test_progress_events_emitted_before_done(self):
        with (
            patch(_LOAD_PROMPT, new=AsyncMock(return_value=MOCK_PROMPT)),
            patch(_RESOLVE, return_value=_mock_provider([VALID_JSON_RESPONSE])),
            patch(_AUDIT, new=AsyncMock()),
            patch(_RATE, new=AsyncMock(return_value=(True, 0))),
            patch(_GET_SETTINGS, new=AsyncMock(return_value=None)),
        ):
            response = self.client.get("/api/v1/ai/parse-budget/stream?text=test")

        lines = response.text.splitlines()
        progress_indices = [i for i, line in enumerate(lines) if line == "event: progress"]
        done_index = next(i for i, line in enumerate(lines) if line == "event: done")
        assert len(progress_indices) >= 1
        assert all(i < done_index for i in progress_indices)

    def test_done_event_contains_valid_json(self):
        with (
            patch(_LOAD_PROMPT, new=AsyncMock(return_value=MOCK_PROMPT)),
            patch(_RESOLVE, return_value=_mock_provider([VALID_JSON_RESPONSE])),
            patch(_AUDIT, new=AsyncMock()),
            patch(_RATE, new=AsyncMock(return_value=(True, 0))),
            patch(_GET_SETTINGS, new=AsyncMock(return_value=None)),
        ):
            response = self.client.get("/api/v1/ai/parse-budget/stream?text=test")

        assert "event: done" in response.text
        lines = response.text.splitlines()
        done_data = next(lines[i + 1] for i, line in enumerate(lines) if line == "event: done")
        payload = json.loads(done_data[len("data: "):])
        assert payload["budget_name"] == "Staff Grant"
        assert payload["ai_available"] is True
        assert payload["prompt_version"] == "v1"

    def test_error_event_sent_on_invalid_llm_output(self):
        with (
            patch(_LOAD_PROMPT, new=AsyncMock(return_value=MOCK_PROMPT)),
            patch(_RESOLVE, return_value=_mock_provider(["not valid json at all"])),
            patch(_AUDIT, new=AsyncMock()),
            patch(_RATE, new=AsyncMock(return_value=(True, 0))),
            patch(_GET_SETTINGS, new=AsyncMock(return_value=None)),
        ):
            response = self.client.get("/api/v1/ai/parse-budget/stream?text=test")

        assert response.status_code == 200
        assert "event: error" in response.text

    def test_unavailable_event_when_prompt_load_fails(self):
        with (
            patch(_LOAD_PROMPT, new=AsyncMock(side_effect=ValueError("no prompt"))),
            patch(_RESOLVE, return_value=_mock_provider([])),
            patch(_RATE, new=AsyncMock(return_value=(True, 0))),
            patch(_GET_SETTINGS, new=AsyncMock(return_value=None)),
        ):
            response = self.client.get("/api/v1/ai/parse-budget/stream?text=test")

        assert response.status_code == 200
        assert "event: unavailable" in response.text

    def test_audit_log_written_with_prompt_version_and_provider(self):
        mock_audit = AsyncMock()
        with (
            patch(_LOAD_PROMPT, new=AsyncMock(return_value=MOCK_PROMPT)),
            patch(_RESOLVE, return_value=_mock_provider([VALID_JSON_RESPONSE])),
            patch(_AUDIT, mock_audit),
            patch(_RATE, new=AsyncMock(return_value=(True, 0))),
            patch(_GET_SETTINGS, new=AsyncMock(return_value=None)),
        ):
            self.client.get("/api/v1/ai/parse-budget/stream?text=test")

        mock_audit.assert_called_once()
        kwargs = mock_audit.call_args.kwargs
        assert kwargs["prompt_version"] == "v1"
        assert kwargs["provider"] == "ollama"
