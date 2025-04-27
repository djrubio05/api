"""add foreign key to posts table

Revision ID: 06816c574a4f
Revises: 15f5760239de
Create Date: 2025-04-27 00:15:47.525109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '06816c574a4f'
down_revision: Union[str, None] = '15f5760239de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key(
        'fk_posts_users',
        'posts',
        'users',
        ['owner_id'],
        ['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'fk_posts_users',
        'posts',
        type_='foreignkey'
    )
    pass
