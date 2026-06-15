import anyio
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.audit import write_audit_log
from app.models.audit_log import AIAuditLog


COMMON_KWARGS = dict(
    customer_id="aaaaaaaa-0000-0000-0000-000000000001",
    user_id="bbbbbbbb-0000-0000-0000-000000000002",
    prompt_version="none",
    input_text="We need $10k for staff salaries and $5k for supplies",
    provider="none",
    model="",
    success=True,
    duration_ms=42,
)


def _make_mock_session():
    """Returns (mock_session, async_session_class) for patching AsyncSessionLocal."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session_class = MagicMock()
    mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_class.return_value.__aexit__ = AsyncMock(return_value=False)
    return mock_session, mock_session_class


def _patched_write(**kwargs):
    mock_session, mock_session_class = _make_mock_session()

    async def _run():
        await write_audit_log(**kwargs)

    with patch("app.services.audit.AsyncSessionLocal", mock_session_class):
        anyio.run(_run)

    return mock_session


class TestAuditLogWrite:
    def test_successful_parse_writes_audit_row_with_customer_and_user_id(self):
        mock_session = _patched_write(**COMMON_KWARGS)

        mock_session.add.assert_called_once()
        log: AIAuditLog = mock_session.add.call_args[0][0]
        assert isinstance(log, AIAuditLog)
        assert str(log.customer_id) == COMMON_KWARGS["customer_id"]
        assert str(log.user_id) == COMMON_KWARGS["user_id"]
        assert log.success is True
        mock_session.commit.assert_called_once()

    def test_failed_parse_writes_audit_row_with_success_false(self):
        mock_session = _patched_write(
            **{**COMMON_KWARGS, "success": False, "error_message": "parse_failed"}
        )

        log: AIAuditLog = mock_session.add.call_args[0][0]
        assert log.success is False
        assert log.error_message == "parse_failed"

    def test_audit_row_includes_token_counts(self):
        mock_session = _patched_write(
            **{**COMMON_KWARGS, "input_tokens": 15, "output_tokens": 80}
        )

        log: AIAuditLog = mock_session.add.call_args[0][0]
        assert isinstance(log.input_tokens, int)
        assert isinstance(log.output_tokens, int)
        assert log.input_tokens == 15
        assert log.output_tokens == 80

    def test_audit_row_has_id_default_and_created_at(self):
        mock_session = _patched_write(**COMMON_KWARGS)

        log: AIAuditLog = mock_session.add.call_args[0][0]
        # id default fires at INSERT (SQLAlchemy flush), not at object construction;
        # verify the column has a callable default configured
        id_col = AIAuditLog.__table__.c["id"]
        assert id_col.default is not None
        assert callable(id_col.default.arg)
        assert log.created_at is not None
