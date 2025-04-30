"""add content column to posts table

Revision ID: 90be867d9cd5
Revises: 9ee2bf81ea4c
Create Date: 2025-04-29 20:58:16.990153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90be867d9cd5'
down_revision: Union[str, None] = '9ee2bf81ea4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","content")
    pass
