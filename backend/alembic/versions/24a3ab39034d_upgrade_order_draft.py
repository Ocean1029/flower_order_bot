"""upgrade order draft (SQLite-compatible)

Revision ID: 24a3ab39034d
Revises: 63bb1ccf4d1a
Create Date: 2025-05-15 16:38:20.581300
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '24a3ab39034d'
down_revision = '63bb1ccf4d1a'
branch_labels = None
depends_on = None


def has_column(connection, table_name: str, column_name: str) -> bool:
    inspector = Inspector.from_engine(connection)
    columns = inspector.get_columns(table_name)
    return any(col["name"] == column_name for col in columns)

def has_column(connection, table_name: str, column_name: str) -> bool:
    inspector = Inspector.from_engine(connection)
    columns = inspector.get_columns(table_name)
    return any(col["name"] == column_name for col in columns)


def upgrade() -> None:
    conn = op.get_bind()

    if not has_column(conn, "order_draft", "receiver_user_id"):
        op.add_column("order_draft", sa.Column("receiver_user_id", sa.Integer(), nullable=True))

    if not has_column(conn, "order_draft", "item_type"):
        op.add_column("order_draft", sa.Column("item_type", sa.String(), nullable=True))

    if not has_column(conn, "order_draft", "product_name"):
        op.add_column("order_draft", sa.Column("product_name", sa.Text(), nullable=True))

    if not has_column(conn, "order_draft", "quantity"):
        op.add_column("order_draft", sa.Column("quantity", sa.Integer(), nullable=True))

    if not has_column(conn, "order_draft", "total_amount"):
        op.add_column("order_draft", sa.Column("total_amount", sa.Numeric(10, 2), nullable=True))

    if not has_column(conn, "order_draft", "notes"):
        op.add_column("order_draft", sa.Column("notes", sa.Text(), nullable=True))

    if not has_column(conn, "order_draft", "card_message"):
        op.add_column("order_draft", sa.Column("card_message", sa.Text(), nullable=True))

    if not has_column(conn, "order_draft", "shipment_method"):
        op.add_column("order_draft", sa.Column("shipment_method", sa.String(), nullable=True))  # 原 Enum

    if not has_column(conn, "order_draft", "shipment_status"):
        op.add_column("order_draft", sa.Column("shipment_status", sa.String(), nullable=True))  # 原 Enum

    if not has_column(conn, "order_draft", "receipt_address"):
        op.add_column("order_draft", sa.Column("receipt_address", sa.String(), nullable=True))

    if not has_column(conn, "order_draft", "delivery_address"):
        op.add_column("order_draft", sa.Column("delivery_address", sa.Text(), nullable=True))

    if not has_column(conn, "order_draft", "delivery_datetime"):
        op.add_column("order_draft", sa.Column("delivery_datetime", sa.DateTime(), nullable=True))

def downgrade() -> None:
    op.drop_column('order_draft', 'delivery_datetime')
    op.drop_column('order_draft', 'delivery_address')
    op.drop_column('order_draft', 'receipt_address')
    op.drop_column('order_draft', 'shipment_status')
    op.drop_column('order_draft', 'shipment_method')
    op.drop_column('order_draft', 'card_message')
    op.drop_column('order_draft', 'notes')
    op.drop_column('order_draft', 'total_amount')
    op.drop_column('order_draft', 'quantity')
    op.drop_column('order_draft', 'product_name')
    op.drop_column('order_draft', 'item_type')
    op.drop_column('order_draft', 'receiver_user_id')
