from datetime import datetime, timedelta, timezone
from celery_app import app
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url

_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        from config import settings

        url = make_url(settings.AI_DATABASE_URL).set(drivername="postgresql+psycopg2")
        _engine = create_engine(url)
    return _engine


def _cleanup(engine=None):
    if engine is None:
        engine = _get_engine()
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    with engine.begin() as conn:
        result = conn.execute(
            text(
                "DELETE FROM ai_chat_sessions "
                "WHERE last_activity_at < :cutoff OR message_count > :max_messages "
                "RETURNING id"
            ),
            {"cutoff": cutoff, "max_messages": 50},
        )
        return {"deleted": result.rowcount}


@app.task(name="tasks.ai.cleanup_sessions")
def run():
    return _cleanup()
