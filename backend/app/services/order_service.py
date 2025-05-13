from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import Order
from app.models.user import User
from app.models.logistics import Shipment

async def get_all_orders(session: AsyncSession) -> list:
    result = []

    orders_result = await session.execute(select(Order))
    orders = orders_result.scalars().all()

    for o in orders:
        user_result = await session.execute(select(User).filter_by(id=o.user_id))
        user = user_result.scalar_one_or_none()

        shipment_result = await session.execute(select(Shipment).filter_by(order_id=o.id))
        shipment = shipment_result.scalar_one_or_none()

        result.append({
            "id": o.id,
            "customer_name": user.name if user else "未知",
            "phone": user.phone if user else "",
            "item_type": o.item_type,
            "product_name": o.product_name,
            "quantity": o.quantity,
            "total_amount": float(o.total_amount) if o.total_amount else None,
            "note": o.notes or "",
            "pickup_method": shipment.method if shipment else "未知",
            "pickup_datetime": shipment.delivery_datetime.strftime("%Y-%m-%d %H:%M") if shipment and shipment.delivery_datetime else "",
        })

    return result
