"""add column to my list

Revision ID: 458b13fad34br
Revises: d58ab442fa20
Create Date: 2025-04-30 12:06:56.519012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '458b13fad34b'
down_revision: Union[str, None] = 'd58ab442fa20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("published",sa.Boolean(),nullable=False,server_default="TRUE"))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("NOW()")))
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
