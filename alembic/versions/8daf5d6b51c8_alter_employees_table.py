"""alter employees table

Revision ID: 8daf5d6b51c8
Revises: 
Create Date: 2025-10-29 10:43:47.863992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8daf5d6b51c8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    query = "alter table employees add column gender varchar(50) default 'male'"
    op.execute(query)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    query = "alter table employees drop column gender"
    op.execute(query)
    pass
