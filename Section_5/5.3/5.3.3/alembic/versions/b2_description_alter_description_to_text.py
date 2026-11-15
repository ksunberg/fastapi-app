"""Alter description to Text

Revision ID: b2_description
Revises: 01aca821edf0
Create Date: 2026-11-15 13:14:01.350007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2_description'
down_revision: Union[str, Sequence[str], None] = '01aca821edf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        '5.3.3',
        'description',
        existing_type=sa.String(),
        type_=sa.Text(),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        '5.3.3',
        'description',
        existing_type=sa.Text(),
        type_=sa.String(),
        nullable=False,
    )
