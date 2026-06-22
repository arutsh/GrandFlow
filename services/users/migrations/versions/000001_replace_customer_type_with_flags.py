"""Replace CustomerType enum with is_ngo / is_donor boolean flags

Revision ID: 000001
Revises: 15c513b8d0f9
Create Date: 2026-06-19 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "000001"
down_revision: Union[str, Sequence[str], None] = "15c513b8d0f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = {c["name"] for c in inspector.get_columns("customers")}

    if "is_ngo" not in columns:
        op.add_column(
            "customers",
            sa.Column("is_ngo", sa.Boolean(), nullable=False, server_default="false"),
        )
    if "is_donor" not in columns:
        op.add_column(
            "customers",
            sa.Column("is_donor", sa.Boolean(), nullable=False, server_default="false"),
        )

    if "type" in columns:
        op.execute("UPDATE customers SET is_ngo = true WHERE type = 'ngo'")
        op.execute("UPDATE customers SET is_donor = true WHERE type = 'donor'")
        op.drop_column("customers", "type")
        op.execute("DROP TYPE IF EXISTS customertype")


def downgrade() -> None:
    op.execute("CREATE TYPE customertype AS ENUM ('donor', 'ngo')")
    op.add_column(
        "customers",
        sa.Column(
            "type",
            sa.Enum("donor", "ngo", name="customertype", create_type=False),
            nullable=False,
            server_default="ngo",
        ),
    )
    op.execute("UPDATE customers SET type = 'ngo' WHERE is_ngo = true AND is_donor = false")
    op.execute("UPDATE customers SET type = 'donor' WHERE is_donor = true AND is_ngo = false")
    # Subgranting orgs (both flags true) default to 'ngo' — lossy downgrade
    op.drop_column("customers", "is_donor")
    op.drop_column("customers", "is_ngo")
