"""add audit fields

Revision ID: 62b49e9e203c
Revises: 052d75844324
Create Date: 2025-08-27 17:18:27.250686

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "62b49e9e203c"
down_revision: Union[str, Sequence[str], None] = "052d75844324"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("budgets", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("budgets", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("budgets", sa.Column("created_by", sa.String(), nullable=True))
    op.add_column("budgets", sa.Column("updated_by", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("budgets", "created_at")
    op.drop_column("budgets", "updated_at")
    op.drop_column("budgets", "created_by")
    op.drop_column("budgets", "updated_by")
