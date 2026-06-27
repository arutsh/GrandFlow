"""Create ai_chat_sessions table

Revision ID: 004_create_ai_chat_sessions
Revises: 003_create_user_ai_settings
Create Date: 2026-06-27 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import shared

revision: str = "004_create_ai_chat_sessions"
down_revision: Union[str, Sequence[str], None] = "003_create_user_ai_settings"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ai_chat_sessions",
        sa.Column("id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("customer_id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("user_id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("title", sa.String(255), nullable=True),
        sa.Column("message_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ai_chat_sessions_customer_id"),
        "ai_chat_sessions",
        ["customer_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ai_chat_sessions_user_id"),
        "ai_chat_sessions",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_ai_chat_sessions_last_activity_at",
        "ai_chat_sessions",
        ["last_activity_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_ai_chat_sessions_last_activity_at", table_name="ai_chat_sessions")
    op.drop_index(op.f("ix_ai_chat_sessions_user_id"), table_name="ai_chat_sessions")
    op.drop_index(op.f("ix_ai_chat_sessions_customer_id"), table_name="ai_chat_sessions")
    op.drop_table("ai_chat_sessions")
