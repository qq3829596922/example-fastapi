"""create posts table

Revision ID: 9ee2bf81ea4c
Revises: 
Create Date: 2025-04-29 20:37:42.860721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ee2bf81ea4c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",
    sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
    sa.Column("title",sa.String(),nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
