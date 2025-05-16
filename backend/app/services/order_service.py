# app/services/order_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional

from app.models.user import User
from app.models.order import Order, OrderDraft

from app.schemas.order import OrderOut, OrderDraftOut, OrderDraftUpdate
from app.services.payment_service import get_pay_way_by_order_id
from app.services.user_service import get_user_by_id
from app.enums.order import OrderStatus, OrderDraftStatus


async def get_all_orders(db: AsyncSession) -> Optional[List[OrderOut]]:
    results = []

    # 撈出所有訂單
    order_stmt = select(Order)
    order_result = await db.execute(order_stmt)
    orders = order_result.scalars().all()

    for order in orders:
        user = await get_user_by_id(db, order.user_id)
        receiver_user = await get_user_by_id(db, order.receiver_user_id)
        pay_way = await get_pay_way_by_order_id(db, order.id)
        
        if(not user):
            print(f"User not found for order {order.id}")
            continue
        

        results.append(OrderOut(
            id=order.id,
            customer_name=user.name,
            customer_phone=user.phone,
            receiver_name=receiver_user.name if receiver_user else user.name,
            receiver_phone=receiver_user.phone if receiver_user else user.phone,

            order_date=order.created_at,
            order_status=order.status,
            
            pay_way=pay_way,
            total_amount=order.total_amount,
            
            item=order.item_type,
            quantity=order.quantity,
            note=order.notes,
            card_message=order.card_message,
            
            shipment_method=order.shipment_method,
            weekday=order.created_at.strftime("%A"),
            send_datetime=order.delivery_datetime or order.created_at, # TODO fix datetime error
            receipt_address=order.receipt_address,
            delivery_address=order.delivery_address or order.receipt_address or ""
        ))

    return results

async def get_order_draft_by_room_id(db: AsyncSession, room_id: int) -> Optional[OrderDraftOut]:
    stmt = (
        select(OrderDraft)
        .where(OrderDraft.room_id == room_id)
        .where(OrderDraft.status == OrderDraftStatus.COLLECTING)
        .order_by(OrderDraft.created_at.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    order_draft = result.scalar_one_or_none()
    
    user = await get_user_by_id(db, order_draft.user_id) if order_draft else None
    receiver_user = await get_user_by_id(db, order_draft.receiver_user_id) if order_draft else None
    pay_way = await get_pay_way_by_order_id(db, order_draft.id) if order_draft else None

    if order_draft:
        return OrderDraftOut(
            id=order_draft.id,
            customer_name=user.name if user else "未知",
            customer_phone=user.phone if user else "未知",
            receiver_name=receiver_user.name if receiver_user else user.name,
            receiver_phone=receiver_user.phone if receiver_user else user.phone,

            order_date=order_draft.created_at,
            order_status=order_draft.status,
            
            pay_way=pay_way,
            total_amount=order_draft.total_amount,
            
            item=order_draft.item_type,
            quantity=order_draft.quantity,
            note=order_draft.notes,
            card_message=order_draft.card_message,
            
            shipment_method=order_draft.shipment_method,
            weekday=order_draft.created_at.strftime("%A"),
            send_datetime=order_draft.delivery_datetime or order_draft.created_at, # TODO fix datetime error
            receipt_address=order_draft.receipt_address,
            delivery_address=order_draft.delivery_address or order_draft.receipt_address or ""
        )
    
    return None

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


async def update_order_draft_by_id(
    db: AsyncSession, room_id: int, update_schema: OrderDraftUpdate
) -> Optional[OrderDraftOut]:

    update_data = update_schema.model_dump()
    print(f"update_data: {update_data}")
    
    # if not update_data:
    #     raise ValueError("No update fields provided.")
    # stmt = (
    #     update(OrderDraft)
    #     .where(OrderDraft.room_id == room_id)
    #     .values(**update_data)
    #     .execution_options(synchronize_session="fetch")
    # )

    # await db.execute(stmt)
    # await db.commit()

    return await get_order_draft_by_room_id(db, room_id)