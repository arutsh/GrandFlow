"""Create ai_audit_logs table

Revision ID: 001_create_ai_audit_logs
Revises:
Create Date: 2026-06-15 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import shared

revision: str = "001_create_ai_audit_logs"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ai_audit_logs",
        sa.Column("id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("customer_id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("user_id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("prompt_version", sa.String(), nullable=False),
        sa.Column("input_text", sa.Text(), nullable=False),
        sa.Column("output_json", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("model", sa.String(), nullable=False, server_default=""),
        sa.Column("input_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("output_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_audit_logs_customer_id"), "ai_audit_logs", ["customer_id"], unique=False)
    op.create_index(op.f("ix_ai_audit_logs_user_id"), "ai_audit_logs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_ai_audit_logs_user_id"), table_name="ai_audit_logs")
    op.drop_index(op.f("ix_ai_audit_logs_customer_id"), table_name="ai_audit_logs")
    op.drop_table("ai_audit_logs")
