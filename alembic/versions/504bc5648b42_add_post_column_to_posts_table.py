"""add post column to posts table

Revision ID: 504bc5648b42
Revises: 90be867d9cd5
Create Date: 2025-04-30 11:53:22.017345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '504bc5648b42'
down_revision: Union[str, None] = '90be867d9cd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
    sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
    sa.Column("email",sa.String(),nullable=False),
    sa.Column("password",sa.String(),nullable=False),
    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("NOW()")),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
