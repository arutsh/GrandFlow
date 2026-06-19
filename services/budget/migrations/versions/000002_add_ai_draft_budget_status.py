"""Add ai_draft value to budget_status enum

Revision ID: 000002
Revises: 000001
Create Date: 2026-06-19 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

revision: str = "000002"
down_revision: Union[str, Sequence[str], None] = "000001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ALTER TYPE cannot run inside a transaction block in PostgreSQL
    op.execute("COMMIT")
    op.execute("ALTER TYPE budget_status ADD VALUE IF NOT EXISTS 'ai_draft' BEFORE 'draft'")


def downgrade() -> None:
    # PostgreSQL does not support removing enum values; downgrade is a no-op.
    # To remove ai_draft: recreate the type without it, update all rows, swap types.
    pass
