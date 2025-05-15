"""Make instructions column in payment_method nullable

Revision ID: b6a4d45039f9
Revises: 16811f0a5f64
Create Date: 2025-05-15 15:54:20.583438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6a4d45039f9'
down_revision: Union[str, None] = '16811f0a5f64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('payment_method', schema=None) as batch_op:
        batch_op.alter_column(
            'instructions',
            existing_type=sa.TEXT(),
            nullable=True
        )

def downgrade() -> None:
    with op.batch_alter_table('payment_method', schema=None) as batch_op:
        batch_op.alter_column(
            'instructions',
            existing_type=sa.TEXT(),
            nullable=False
        )
