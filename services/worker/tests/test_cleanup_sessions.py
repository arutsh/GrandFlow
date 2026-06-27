from contextlib import contextmanager
from unittest.mock import MagicMock

from tasks.ai.cleanup_sessions import _cleanup


def test_cleanup_returns_deleted_count():
    mock_result = MagicMock()
    mock_result.rowcount = 3

    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_result

    @contextmanager
    def mock_begin():
        yield mock_conn

    mock_engine = MagicMock()
    mock_engine.begin = mock_begin

    result = _cleanup(engine=mock_engine)
    assert result == {"deleted": 3}


def test_cleanup_passes_correct_params():
    mock_result = MagicMock()
    mock_result.rowcount = 0

    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_result

    @contextmanager
    def mock_begin():
        yield mock_conn

    mock_engine = MagicMock()
    mock_engine.begin = mock_begin

    _cleanup(engine=mock_engine)

    call_kwargs = mock_conn.execute.call_args
    params = call_kwargs[0][1]
    assert "cutoff" in params
    assert params["max_messages"] == 50
