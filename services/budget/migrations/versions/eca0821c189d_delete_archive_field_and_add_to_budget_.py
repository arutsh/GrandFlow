"""delete archive field and add to budget status

Revision ID: eca0821c189d
Revises: 66081a917454
Create Date: 2025-11-23 13:03:45.840002

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "eca0821c189d"
down_revision: Union[str, Sequence[str], None] = "66081a917454"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add new ENUM value to Postgres
    op.execute("ALTER TYPE budget_status ADD VALUE IF NOT EXISTS 'archived'")

    # 2. Drop archived boolean column
    with op.batch_alter_table("budgets", schema=None) as batch_op:
        batch_op.drop_column("archived")


def downgrade() -> None:
    # WARNING: Postgres cannot remove enum values.
    # You must recreate the enum to fully downgrade.
    # Typical safe downgrade just re-adds the dropped column.

    with op.batch_alter_table("budgets", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("archived", sa.Boolean(), nullable=False, server_default=sa.text("false"))
        )

    # Full enum downgrade would require recreation:
    # Skipping because it's destructive and usually unnecessary.
