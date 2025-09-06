"""creating new AuditMixin

Revision ID: 052d75844324
Revises: b48f65c75af9
Create Date: 2025-08-27 17:14:55.335712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '052d75844324'
down_revision: Union[str, Sequence[str], None] = 'b48f65c75af9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
