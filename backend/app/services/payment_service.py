
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Optional
from app.models.payment import Payment, PaymentMethod
from app.schemas.payment import PaymentMethodBase


async def get_all_payment_methods(db: AsyncSession) -> Optional[list[PaymentMethodBase]]:

    payment_stmt = select(PaymentMethod)
    payment_result = await db.execute(payment_stmt)
    payment_methods = payment_result.scalars().all()

    return [
        PaymentMethodBase(
            id=method.id,
            code=method.code,
            display_name=method.display_name,
            display_image_url=method.display_image_url,
            instructions=method.instructions,
            requires_manual_confirm=method.requires_manual_confirm,
            active=method.active,
        )
        for method in payment_methods
    ]


async def get_pay_way_by_order_id(db: AsyncSession, order_id: int) -> str:
    payment_stmt = (
        select(Payment, PaymentMethod)
        .join(PaymentMethod, Payment.method_id == PaymentMethod.id)
        .where(Payment.order_id == order_id)
        .limit(1)
    )
    payment_result = await db.execute(payment_stmt)
    payment = payment_result.first()
    if payment is None:
        return "Unknown"
    payment_method = payment[1]
    return payment_method.display_name