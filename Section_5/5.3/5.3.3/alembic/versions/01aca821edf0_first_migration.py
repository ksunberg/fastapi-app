"""First migration

Revision ID: 01aca821edf0
Revises: 
Create Date: 2026-11-15 13:07:46.203258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '01aca821edf0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    product_status = postgresql.ENUM(
        'draft', 'published', 'archived', 'deprecated',
        name='product_status',
        create_type=False,
    )
    product_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        '5.3.3',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('count', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), server_default='', nullable=False),
        sa.Column('status', product_status, server_default='draft', nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('5.3.3')
    postgresql.ENUM(name='product_status').drop(op.get_bind(), checkfirst=True)
