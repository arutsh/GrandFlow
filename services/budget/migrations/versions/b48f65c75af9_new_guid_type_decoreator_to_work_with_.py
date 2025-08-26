"""new GUID type decoreator to work with different db

Revision ID: b48f65c75af9
Revises: 9f2088bca40c
Create Date: 2025-08-26 17:18:48.991387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b48f65c75af9'
down_revision: Union[str, Sequence[str], None] = '9f2088bca40c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
