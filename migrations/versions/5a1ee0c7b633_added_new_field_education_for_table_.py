"""added new field education for table users

Revision ID: 5a1ee0c7b633
Revises: a3f4888d7478
Create Date: 2025-01-25 18:04:08.925897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a1ee0c7b633'
down_revision: Union[str, None] = 'a3f4888d7478'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('education', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'education')
    # ### end Alembic commands ###
