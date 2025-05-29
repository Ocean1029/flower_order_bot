"""update_datetime_to_timezone

Revision ID: 565a8ea173f6
Revises: cca7fe79ed39
Create Date: 2025-05-29 20:46:44.648938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '565a8ea173f6'
down_revision: Union[str, None] = 'cca7fe79ed39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # notification table
    with op.batch_alter_table('notification') as batch_op:
        batch_op.alter_column('send_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    
    # audit_log table
    with op.batch_alter_table('audit_log') as batch_op:
        batch_op.alter_column('logged_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    
    # chat_room table
    with op.batch_alter_table('chat_room') as batch_op:
        batch_op.alter_column('last_message_ts',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    
    # chat_message table
    with op.batch_alter_table('chat_message') as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    
    # order_draft table
    with op.batch_alter_table('order_draft') as batch_op:
        batch_op.alter_column('delivery_datetime',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    
    # order table
    with op.batch_alter_table('order') as batch_op:
        batch_op.alter_column('delivery_datetime',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    
    # payment table
    with op.batch_alter_table('payment') as batch_op:
        batch_op.alter_column('paid_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
        batch_op.alter_column('confirmed_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # payment table
    with op.batch_alter_table('payment') as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('confirmed_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True)
        batch_op.alter_column('paid_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True)
    
    # order table
    with op.batch_alter_table('order') as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('delivery_datetime',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True)
    
    # order_draft table
    with op.batch_alter_table('order_draft') as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('delivery_datetime',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True)
    
    # chat_message table
    with op.batch_alter_table('chat_message') as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
    
    # chat_room table
    with op.batch_alter_table('chat_room') as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('last_message_ts',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True)
    
    # audit_log table
    with op.batch_alter_table('audit_log') as batch_op:
        batch_op.alter_column('logged_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
    
    # notification table
    with op.batch_alter_table('notification') as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('send_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True)
    # ### end Alembic commands ###
