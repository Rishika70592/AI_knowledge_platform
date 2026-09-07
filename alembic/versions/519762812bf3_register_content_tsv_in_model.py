"""register content_tsv in model

Revision ID: 519762812bf3
Revises: 473d4de1d015
Create Date: 2026-09-07 15:01:52.099897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '519762812bf3'
down_revision: Union[str, Sequence[str], None] = '473d4de1d015'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Intentionally left blank — content_tsv and its GIN index already
    # exist in the database (created manually). This migration exists
    # only to sync Alembic's history; no actual schema change needed.
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
