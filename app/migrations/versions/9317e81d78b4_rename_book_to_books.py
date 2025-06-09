"""rename book to books

Revision ID: 9317e81d78b4
Revises: f88d856f9611
Create Date: 2025-06-09 02:01:22.513033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9317e81d78b4'
down_revision: Union[str, None] = 'f88d856f9611'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('Borrow', 'borrow')
    op.rename_table('librarians', 'librarian')

def downgrade() -> None:
    """Downgrade schema."""
    pass
