"""adding budgetmodel id back

Revision ID: 0bbed460027e
Revises: 1bef72e04f52
Create Date: 2025-09-10 16:45:56.722688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bbed460027e'
down_revision: Union[str, Sequence[str], None] = '1bef72e04f52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
