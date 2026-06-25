"""Initial Migration

Revision ID: 15c513b8d0f9
Revises:
Create Date: 2026-06-05 10:55:03.792656

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
import shared

# revision identifiers, used by Alembic.
revision: str = "15c513b8d0f9"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # userstatus enum — safe to create; skipped if already exists
    op.execute(
        "DO $$ BEGIN "
        "IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userstatus') THEN "
        "CREATE TYPE userstatus AS ENUM ('active', 'pending', 'disabled'); "
        "END IF; END $$"
    )

    # customers — type column intentionally omitted; migration 000001 handles it
    op.create_table(
        "customers",
        sa.Column("id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        if_not_exists=True,
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_customers_id ON customers (id)")

    op.create_table(
        "users",
        sa.Column("id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("first_name", sa.String(), server_default=sa.text("''"), nullable=False),
        sa.Column("last_name", sa.String(), server_default=sa.text("''"), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("customer_id", shared.db.type_decorators.GUID(), nullable=True),
        sa.Column(
            "status",
            PgEnum("active", "pending", "disabled", name="userstatus", create_type=False),
            server_default=sa.text("'pending'"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.PrimaryKeyConstraint("id"),
        if_not_exists=True,
    )
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_id ON users (id)")

    op.create_table(
        "user_sessions",
        sa.Column("id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("user_id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("issued_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column("refresh_token_hash", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        if_not_exists=True,
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_user_sessions_id ON user_sessions (id)")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_user_sessions_id")
    op.drop_table("user_sessions")
    op.execute("DROP INDEX IF EXISTS ix_users_id")
    op.execute("DROP INDEX IF EXISTS ix_users_email")
    op.drop_table("users")
    op.execute("DROP INDEX IF EXISTS ix_customers_id")
    op.drop_table("customers")
