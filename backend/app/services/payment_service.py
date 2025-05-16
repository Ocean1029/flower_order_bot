
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from typing import Optional
from app.models.payment import Payment, PaymentMethod
from app.schemas.payment import PaymentMethodBase


def payment_method_to_base(method) -> PaymentMethodBase:
    return PaymentMethodBase(
        id=method.id,
        code=method.code,
        display_name=method.display_name,
        display_image_url=method.display_image_url,
        instructions=method.instructions,
        requires_manual_confirm=method.requires_manual_confirm,
        active=method.active,
    )

async def get_all_payment_methods(db: AsyncSession) -> Optional[list[PaymentMethodBase]]:
    payment_stmt = select(PaymentMethod)
    payment_result = await db.execute(payment_stmt)
    payment_methods = payment_result.scalars().all()

    return [
        payment_method_to_base(method) for method in payment_methods if method.active
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

async def get_payment_method_by_id(db: AsyncSession, payment_method_id: int) -> Optional[PaymentMethod]:
    stmt = select(PaymentMethod).where(PaymentMethod.id == payment_method_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def toggle_payment_method_active(db: AsyncSession, payment_method_id: int) -> Optional[PaymentMethodBase]:
    payment_method = await get_payment_method_by_id(db, payment_method_id) 
    if not payment_method:
        return None
    payment_method.active = not payment_method.active
    await db.commit()
    await db.refresh(payment_method)
    return payment_method_to_base(payment_method)