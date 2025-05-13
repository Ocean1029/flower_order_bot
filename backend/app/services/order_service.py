# app/services/order_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import Order
from app.models.user import User
from app.models.logistics import Shipment, ShipmentMethod
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

        # 撈出貨資訊
        shipment_stmt = select(Shipment).where(Shipment.order_id == order.id)
        shipment_result = await db.execute(shipment_stmt)
        shipment = shipment_result.scalar_one_or_none()

        receiver_user = None
        if shipment:
            receiver_stmt = select(User).where(User.id == shipment.receiver_user_id)
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
            receipt_address=order.receipt_address,
            order_date=order.created_at,
            total_amount=order.total_amount,
            item=order.item_type,
            quantity=order.quantity,
            note=order.notes,
            pay_way=pay_way,
            card_message=order.card_message,
            weekday=order.created_at.strftime("%A"),
            send_datetime = shipment.delivery_datetime if shipment else order.created_at,
            receiver_name = receiver_user.name if receiver_user else user.name,
            receiver_phone = receiver_user.phone if receiver_user else user.phone,
            delivery_address = shipment.address if shipment else order.receipt_address,
            order_status=order.status,
            shipment_method=shipment.method
        ))

    return results
