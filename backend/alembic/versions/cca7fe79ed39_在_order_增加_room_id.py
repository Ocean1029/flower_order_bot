"""在 order 增加 room id

Revision ID: cca7fe79ed39
Revises: 54daffd2c4ec
Create Date: 2025-05-29 12:08:51.002714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cca7fe79ed39'
down_revision: Union[str, None] = '54daffd2c4ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order') as batch_op:
        batch_op.add_column(sa.Column('room_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_order_room_id', 'chat_room', ['room_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order') as batch_op:
        batch_op.drop_constraint('fk_order_room_id', type_='foreignkey')
        batch_op.drop_column('room_id')
    # ### end Alembic commands ###
