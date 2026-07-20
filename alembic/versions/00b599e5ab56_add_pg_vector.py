"""add pg_vector

Revision ID: 00b599e5ab56
Revises: 5a330beaa413
Create Date: 2026-07-20 13:18:31.291865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '00b599e5ab56'
down_revision: Union[str, Sequence[str], None] = '5a330beaa413'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP EXTENSION IF NOT EXISTS vector;")
