"""added new field for news model

Revision ID: a3f4888d7478
Revises: dd556b610ffc
Create Date: 2025-01-23 23:02:58.908899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3f4888d7478'
down_revision: Union[str, None] = 'dd556b610ffc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('test_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('news', 'test_url')
    # ### end Alembic commands ###
