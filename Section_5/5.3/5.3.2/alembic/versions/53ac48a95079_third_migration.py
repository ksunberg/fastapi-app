"""Third migration

Revision ID: 53ac48a95079
Revises: 172e9986aa62
Create Date: 2026-11-15 11:46:10.414825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53ac48a95079'
down_revision: Union[str, Sequence[str], None] = '172e9986aa62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE product_status ADD VALUE IF NOT EXISTS 'deprecated' AFTER 'archived'")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('UPDATE "5_3_2" SET status = \'draft\' WHERE status = \'deprecated\'')
    op.execute("ALTER TYPE product_status RENAME TO product_status_old")
    op.execute("CREATE TYPE product_status AS ENUM ('draft', 'published', 'archived')")
    op.execute(
        """
        ALTER TABLE "5_3_2"
        ALTER COLUMN status DROP DEFAULT,
        ALTER COLUMN status TYPE product_status
        USING status::text::product_status,
        ALTER COLUMN status SET DEFAULT 'draft'
        """
    )
    op.execute("DROP TYPE product_status_old")
