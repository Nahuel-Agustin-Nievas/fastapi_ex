"""add last few columns to post table

Revision ID: f52e87c35631
Revises: 741b328174c5
Create Date: 2026-01-23 19:33:56.826581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f52e87c35631'
down_revision: Union[str, Sequence[str], None] = '741b328174c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'created_at')
    pass
