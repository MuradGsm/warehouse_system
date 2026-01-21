"""stock updated_at default now

Revision ID: f6344e77b8f1
Revises: 4248666d5b14
Create Date: 2026-01-21 23:19:00.986145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6344e77b8f1'
down_revision: Union[str, Sequence[str], None] = '4248666d5b14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
