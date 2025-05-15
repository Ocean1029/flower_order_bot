"""remove shipment

Revision ID: 16811f0a5f64
Revises: d584f727dd73
Create Date: 2025-05-15 15:17:56.949737

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16811f0a5f64'
down_revision: Union[str, None] = 'd584f727dd73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 清理可能存在的臨時表
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    if '_alembic_tmp_order' in tables:
        op.execute('DROP TABLE _alembic_tmp_order')
    
    # 檢查並添加新欄位（如果不存在）
    columns = [col['name'] for col in inspector.get_columns('order')]
    
    # 1. 添加新欄位（如果不存在）
    with op.batch_alter_table('order') as batch_op:
        if 'receiver_user_id' not in columns:
            batch_op.add_column(sa.Column('receiver_user_id', sa.Integer(), nullable=True))
        
        if 'shipment_method' not in columns:
            batch_op.add_column(sa.Column('shipment_method', sa.String(), nullable=True))
        
        if 'shipment_status' not in columns:
            batch_op.add_column(sa.Column('shipment_status', sa.String(), nullable=True))
        
        if 'delivery_address' not in columns:
            batch_op.add_column(sa.Column('delivery_address', sa.Text(), nullable=True))
        
        if 'delivery_datetime' not in columns:
            batch_op.add_column(sa.Column('delivery_datetime', sa.DateTime(), nullable=True))
    
    # 2. 建立外鍵約束（如果不存在）
    constraints = [fk['name'] for fk in inspector.get_foreign_keys('order')]
    if 'fk_order_receiver_user_id_user' not in constraints:
        with op.batch_alter_table('order') as batch_op:
            batch_op.create_foreign_key(
                'fk_order_receiver_user_id_user',
                'user',
                ['receiver_user_id'], ['id']
            )
    
    # 3. 從 shipment 表複製資料到 order 表（如果 shipment 表存在）
    if 'shipment' in tables:
        op.execute("""
            UPDATE "order"
            SET 
                receiver_user_id = (
                    SELECT receiver_user_id 
                    FROM shipment 
                    WHERE shipment.order_id = "order".id
                ),
                shipment_method = (
                    SELECT method 
                    FROM shipment 
                    WHERE shipment.order_id = "order".id
                ),
                shipment_status = (
                    SELECT status 
                    FROM shipment 
                    WHERE shipment.order_id = "order".id
                ),
                delivery_address = (
                    SELECT address 
                    FROM shipment 
                    WHERE shipment.order_id = "order".id
                ),
                delivery_datetime = (
                    SELECT delivery_datetime 
                    FROM shipment 
                    WHERE shipment.order_id = "order".id
                )
            WHERE EXISTS (
                SELECT 1 
                FROM shipment 
                WHERE shipment.order_id = "order".id
            )
        """)
    
    # 4. 設置預設值
    op.execute("""
        UPDATE "order"
        SET 
            receiver_user_id = user_id,
            shipment_method = 'store_pickup',
            shipment_status = 'pending'
        WHERE receiver_user_id IS NULL
    """)
    
    # 5. 設置非空約束
    with op.batch_alter_table('order') as batch_op:
        batch_op.alter_column('receiver_user_id', nullable=False)
        batch_op.alter_column('shipment_method', nullable=False)
        batch_op.alter_column('shipment_status', nullable=False)
    
    # 6. 刪除 shipment 表（如果存在）
    if 'shipment' in tables:
        op.drop_table('shipment')


def downgrade() -> None:
    # 清理可能存在的臨時表
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    if '_alembic_tmp_order' in tables:
        op.execute('DROP TABLE _alembic_tmp_order')
    
    # 1. 重新創建 shipment 表
    op.create_table('shipment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('method', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('receiver_user_id', sa.Integer(), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('delivery_datetime', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
        sa.ForeignKeyConstraint(['receiver_user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 2. 從 order 表複製資料回 shipment 表
    op.execute("""
        INSERT INTO shipment (
            order_id, method, status, receiver_user_id,
            address, delivery_datetime, created_at, updated_at
        )
        SELECT 
            id, shipment_method, shipment_status, receiver_user_id,
            delivery_address, delivery_datetime, created_at, updated_at
        FROM "order"
    """)
    
    # 3. 刪除 order 表中的欄位
    with op.batch_alter_table('order') as batch_op:
        batch_op.drop_constraint('fk_order_receiver_user_id_user', type_='foreignkey')
        batch_op.drop_column('receiver_user_id')
        batch_op.drop_column('shipment_method')
        batch_op.drop_column('shipment_status')
        batch_op.drop_column('delivery_address')
        batch_op.drop_column('delivery_datetime') 