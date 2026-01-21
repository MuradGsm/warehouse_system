"""stock updated_at default now

Revision ID: 32ca04f29842
Revises: f6344e77b8f1
Create Date: 2026-01-21 23:19:05.348916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32ca04f29842'
down_revision: Union[str, Sequence[str], None] = 'f6344e77b8f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column("current_stock", "updated_at", server_default=sa.text("now()"))

def downgrade():
    op.alter_column("current_stock", "updated_at", server_default=None)