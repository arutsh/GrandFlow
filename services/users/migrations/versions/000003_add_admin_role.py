"""Add admin role to users role check constraint

Revision ID: 000003
Revises: 000002
Create Date: 2026-06-24 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

revision: str = "000003"
down_revision: Union[str, Sequence[str], None] = "000002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check")
    op.execute(
        "ALTER TABLE users ADD CONSTRAINT users_role_check "
        "CHECK (role IN ('superuser', 'admin', 'user'))"
    )


def downgrade() -> None:
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check")
    op.execute(
        "ALTER TABLE users ADD CONSTRAINT users_role_check "
        "CHECK (role IN ('superuser', 'user'))"
    )
