"""Add check constraint on users.role

Revision ID: 000002
Revises: 000001
Create Date: 2026-06-22 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

revision: str = "000002"
down_revision: Union[str, Sequence[str], None] = "000001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Idempotent: skip if constraint already exists
    op.execute(
        "DO $$ BEGIN "
        "IF NOT EXISTS ("
        "  SELECT 1 FROM pg_constraint "
        "  WHERE conname = 'users_role_check' AND conrelid = 'users'::regclass"
        ") THEN "
        "ALTER TABLE users ADD CONSTRAINT users_role_check "
        "CHECK (role IN ('superuser', 'user')); "
        "END IF; END $$"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check"
    )
