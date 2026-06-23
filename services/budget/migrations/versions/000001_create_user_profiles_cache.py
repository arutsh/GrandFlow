"""Create user_profiles cache table

Revision ID: 000001
Revises: 641370375898
Create Date: 2026-06-09 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import shared

revision: str = "000001"
down_revision: Union[str, Sequence[str], None] = "641370375898"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user_profiles",
        sa.Column("user_id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=255), nullable=True),
        sa.Column("last_name", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("customer_id", shared.db.type_decorators.GUID(), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column(
            "cached_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index(
        "ix_user_profiles_email",
        "user_profiles",
        ["email"],
        unique=False,
    )
    op.create_index(
        "ix_user_profiles_customer_id",
        "user_profiles",
        ["customer_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_user_profiles_customer_id", table_name="user_profiles")
    op.drop_index("ix_user_profiles_email", table_name="user_profiles")
    op.drop_table("user_profiles")
