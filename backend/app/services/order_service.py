# app/services/order_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import Order
from app.models.user import User
from app.models.payment import Payment, PaymentMethod
from app.schemas.order import OrderOut
from app.enums.order import OrderStatus
from datetime import datetime
from typing import List

async def get_all_orders(db: AsyncSession) -> List[OrderOut]:
    results = []

    # 撈出所有訂單
    order_stmt = select(Order)
    order_result = await db.execute(order_stmt)
    orders = order_result.scalars().all()

    for order in orders:
        # 撈顧客資料
        user_stmt = select(User).where(User.id == order.user_id)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()

        # 撈收件人資料
        receiver_stmt = select(User).where(User.id == order.receiver_user_id)
        receiver_result = await db.execute(receiver_stmt)
        receiver_user = receiver_result.scalar_one_or_none()

        # 撈付款方式（只取第一筆）
        payment_stmt = (
            select(Payment, PaymentMethod)
            .join(PaymentMethod, Payment.method_id == PaymentMethod.id)
            .where(Payment.order_id == order.id)
            .limit(1)
        )
        payment_result = await db.execute(payment_stmt)
        payment = payment_result.first()
        pay_way = payment[1].display_name if payment else "未知"

        results.append(OrderOut(
            id=order.id,
            customer_name=user.name if user else "未知",
            customer_phone=user.phone if user else "",
            receipt_address=order.receipt_address or "",
            order_date=order.created_at,
            total_amount=order.total_amount,
            item=order.item_type,
            quantity=order.quantity,
            note=order.notes,
            pay_way=pay_way,
            card_message=order.card_message,
            weekday=order.created_at.strftime("%A"),
            send_datetime=order.delivery_datetime or order.created_at,
            receiver_name=receiver_user.name if receiver_user else user.name,
            receiver_phone=receiver_user.phone if receiver_user else user.phone,
            delivery_address=order.delivery_address or order.receipt_address or "",
            order_status=order.status,
            shipment_method=order.shipment_method
        ))

    return results

async def create_order(db: AsyncSession, order_data: dict) -> Order:
    order = Order(**order_data)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

async def get_order(db: AsyncSession, order_id: int) -> Order:
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_order(db: AsyncSession, order_id: int, order_data: dict) -> Order:
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    
    if order:
        for key, value in order_data.items():
            setattr(order, key, value)
        await db.commit()
        await db.refresh(order)
    
    return order

async def delete_order(db: AsyncSession, order_id: int) -> bool:
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    
    if order:
        await db.delete(order)
        await db.commit()
        return True
    
    return False
