"""時區敏感

Revision ID: 24cc4a241b98
Revises: 565a8ea173f6
Create Date: 2025-05-29 22:07:07.447961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24cc4a241b98'
down_revision: Union[str, None] = '565a8ea173f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # user table
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    
    # staff_user table
    with op.batch_alter_table('staff_user', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    
    # audit_log table
    with op.batch_alter_table('audit_log', schema=None) as batch_op:
        batch_op.alter_column('logged_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)


def downgrade() -> None:
    # audit_log table
    with op.batch_alter_table('audit_log', schema=None) as batch_op:
        batch_op.alter_column('logged_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
    
    # staff_user table
    with op.batch_alter_table('staff_user', schema=None) as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
    
    # user table
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
    pass
    # ### end Alembic commands ###
