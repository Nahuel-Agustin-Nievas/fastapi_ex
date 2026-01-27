"""add user table

Revision ID: 7b05c33dfc5a
Revises: 6ea880bf1d6f
Create Date: 2026-01-23 12:31:24.844060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b05c33dfc5a'
down_revision: Union[str, Sequence[str], None] = '6ea880bf1d6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )   


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')