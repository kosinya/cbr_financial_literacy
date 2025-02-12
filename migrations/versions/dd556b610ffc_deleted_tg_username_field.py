"""deleted tg_username field

Revision ID: dd556b610ffc
Revises: 64460888b093
Create Date: 2025-01-15 12:56:28.567305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd556b610ffc'
down_revision: Union[str, None] = '64460888b093'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'tg_username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('tg_username', sa.VARCHAR(), nullable=False))
    # ### end Alembic commands ###
