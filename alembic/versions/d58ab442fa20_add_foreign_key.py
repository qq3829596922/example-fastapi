"""add foreign key

Revision ID: d58ab442fa20
Revises: 504bc5648b42
Create Date: 2025-04-30 11:59:30.598491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd58ab442fa20'
down_revision: Union[str, None] = '504bc5648b42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fk",source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts_users_fk",table_name="posts",type_="foreignkey")
    op.drop_column("posts","owner_id")
    pass
