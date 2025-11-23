"""adding status, duration, currency

Revision ID: 66081a917454
Revises: 73d126ddf8ad
Create Date: 2025-11-20 17:08:58.406359
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = "66081a917454"
down_revision: Union[str, Sequence[str], None] = "73d126ddf8ad"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    # --- 1) CREATE ENUM TYPE (SAFE) ---
    status_enum = postgresql.ENUM(
        "draft",
        "confirmed",
        name="budget_status",
        create_type=False,   # Don't auto-create
    )

    # Force-create if missing
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_type WHERE typname = 'budget_status'
            ) THEN
                CREATE TYPE budget_status AS ENUM ('draft', 'confirmed');
            END IF;
        END
        $$;
        """
    )

    # --- 2) ADD COLUMNS WITH TEMP DEFAULTS ---
    op.add_column(
        "budgets",
        sa.Column(
            "duration_months",
            sa.Integer(),
            nullable=True,
            server_default=sa.text("0"),
        ),
    )
    op.add_column(
        "budgets",
        sa.Column(
            "archived",
            sa.Boolean(),
            nullable=True,
            server_default=sa.text("FALSE"),
        ),
    )
    op.add_column(
        "budgets",
        sa.Column(
            "local_currency",
            sa.String(length=3),
            nullable=True,
            server_default=sa.text("'GBP'"),
        ),
    )

    # ENUM column — MUST refer to existing DB type
    op.add_column(
        "budgets",
        sa.Column(
            "status",
            postgresql.ENUM(
                "draft",
                "confirmed",
                name="budget_status",
                create_type=False,
            ),
            nullable=True,
            server_default=sa.text("'draft'::budget_status"),
        ),
    )

    # --- 3) UPDATE EXISTING ROWS ---
    op.execute("UPDATE budgets SET duration_months = 0 WHERE duration_months IS NULL")
    op.execute("UPDATE budgets SET archived = FALSE WHERE archived IS NULL")
    op.execute(
        "UPDATE budgets SET local_currency = 'GBP' WHERE local_currency IS NULL OR local_currency = ''"
    )
    op.execute("UPDATE budgets SET status = 'draft' WHERE status IS NULL")

    # --- 4) MAKE COLUMNS NOT NULL & REMOVE DEFAULTS ---
    op.alter_column("budgets", "duration_months", nullable=False, server_default=None)
    op.alter_column("budgets", "archived", nullable=False, server_default=None)
    op.alter_column("budgets", "local_currency", nullable=False, server_default=None)
    op.alter_column("budgets", "status", nullable=False, server_default=None)


def downgrade() -> None:
    op.drop_column("budgets", "status")
    op.drop_column("budgets", "local_currency")
    op.drop_column("budgets", "archived")
    op.drop_column("budgets", "duration_months")

    op.execute("DROP TYPE IF EXISTS budget_status")
