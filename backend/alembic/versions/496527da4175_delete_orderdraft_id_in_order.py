"""delete orderdraft_id in order

Revision ID: 496527da4175
Revises: 3d78613b88b6
Create Date: 2025-05-27 16:38:09.269417

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '496527da4175'
down_revision: Union[str, None] = '3d78613b88b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order') as batch_op:
        batch_op.drop_column('draft_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order') as batch_op:
        batch_op.add_column(sa.Column('draft_id', sa.INTEGER(), nullable=False))
    # ### end Alembic commands ###
