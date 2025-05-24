# app/services/order_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status

from app.models.user import User
from app.models.order import Order, OrderDraft
from app.models.payment import Payment

from app.schemas.order import OrderOut, OrderDraftOut, OrderDraftUpdate, OrderDraftCreate, OrderCreate
from app.services.payment_service import get_pay_way_by_order_id, get_payment_method_by_id
from app.services.user_service import get_user_by_id, create_user
from app.services.message_service import get_chat_room_by_room_id
from app.enums.order import OrderStatus, OrderDraftStatus

async def get_order(db: AsyncSession, order_id: int) -> Order:
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

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
            
            pay_way_id=pay_way.id if pay_way else None,
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

async def create_order(db: AsyncSession, order_draft: OrderDraft) -> Order:
    # step 1: 根據 order_draft 建立 order
    # step 2: 將 order_draft 的 status 改成 completed
    # step 3: 回傳 order
    pass

# async def update_order(db: AsyncSession, order_id: int, order_data: dict) -> Order:
#     stmt = select(Order).where(Order.id == order_id)
#     result = await db.execute(stmt)
#     order = result.scalar_one_or_none()
    
#     if order:
#         for key, value in order_data.items():
#             setattr(order, key, value)
#         await db.commit()
#         await db.refresh(order)
    
#     return order

async def delete_order(db: AsyncSession, order_id: int) -> bool:
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    
    if order:
        # 把 order 的 status 改成 cancelled
        order.status = OrderStatus.CANCELLED
        await db.commit()
        await db.refresh(order)
        return True
    
    return False

async def get_order_draft(db: AsyncSession, room_id: int) -> Optional[OrderDraft]:
    stmt = (
        select(OrderDraft)
        .where(OrderDraft.room_id == room_id)
        .where(OrderDraft.status == OrderDraftStatus.COLLECTING)
        .order_by(OrderDraft.created_at.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    order_draft = result.scalar_one_or_none()
    
    return order_draft

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
    # 邏輯上，這裡應該是用 order_draft 的付款方式，但目前還沒有實作

    if order_draft:
        return OrderDraftOut(
            id=order_draft.id,
            customer_name=user.name if user else "未知",
            customer_phone=user.phone if user else "未知",
            receiver_name=receiver_user.name if receiver_user else user.name,
            receiver_phone=receiver_user.phone if receiver_user else user.phone,

            order_date=order_draft.created_at,
            order_status=order_draft.status,
            
            pay_way_id=pay_way,
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



async def get_collecting_order_draft(db: AsyncSession, room_id: int) -> Optional[OrderDraft]:
    result = await db.execute(
        select(OrderDraft).where(
            OrderDraft.room_id == room_id,
            OrderDraft.status == OrderDraftStatus.COLLECTING
        ).limit(1)
    )
    return result.scalar_one_or_none()


async def create_order_draft_by_room_id(
    db: AsyncSession,
    room_id: int,
    draft_in: OrderDraftCreate
) -> OrderDraft:
    
    """
    依據 room_id 新建一筆 collecting 狀態的 order_draft
    -----------------------------------------------------------------
    - 若 room_id 查無聊天室 → 404
    - 若該 room 中沒有訂單，或是有 status=COMPLETED 的訂單 → 新建一個新的 order_draft
      若該 room 中已有 status=collecting 的草稿 -> update
    - 回傳 *OrderDraft ORM*，呼叫端可再轉成 Pydantic
    """

    # 1. 取得聊天室
    room = await get_chat_room_by_room_id(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat room with id {room_id} not found."
        )

    # 2. 檢查該聊天室是否有訂單，若沒有則新建一個
    order_draft = await get_collecting_order_draft(db, room_id)
    if not order_draft:
        order_draft = OrderDraft(
            room_id=room.id,
            user_id=room.user_id,
            status=OrderDraftStatus.COLLECTING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(order_draft)
        await db.commit()
        await db.refresh(order_draft)
    
    return await update_order_draft_by_room_id(db, room_id, draft_in)

async def update_order_draft_by_room_id(
    db: AsyncSession, room_id: int, draft_in: OrderDraftUpdate
) -> OrderDraftOut:
    
    # 1. 取得聊天室
    room = await get_chat_room_by_room_id(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat room with id {room_id} not found."
        )

    order_draft = await get_collecting_order_draft(db, room_id)
    if not order_draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order draft with room id {room_id} not found."
        )
    
    # 4. 填入草稿資訊
    if draft_in.item is not None:
        order_draft.item_type = draft_in.item
    if draft_in.quantity is not None:
        order_draft.quantity = draft_in.quantity
    if draft_in.total_amount is not None:
        order_draft.total_amount = draft_in.total_amount
    if draft_in.note is not None:
        order_draft.notes = draft_in.note
    if draft_in.card_message is not None:
        order_draft.card_message = draft_in.card_message
    if draft_in.shipment_method is not None:
        order_draft.shipment_method = draft_in.shipment_method
    if draft_in.send_datetime is not None:
        order_draft.delivery_datetime = draft_in.send_datetime
    if draft_in.receipt_address is not None:
        order_draft.receipt_address = draft_in.receipt_address
    if draft_in.delivery_address is not None:
        order_draft.delivery_address = draft_in.delivery_address
    order_draft.updated_at = datetime.utcnow()

    # 5. 新增收件人資訊
    if draft_in.receiver_name or draft_in.receiver_phone:
        # just create the receiver user directly, TODO: Add a "order relation" table to store the relation between the customer and receiver
        receiver_user = User(
            name=draft_in.receiver_name,
            phone=draft_in.receiver_phone,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(receiver_user)
        await db.commit()
        await db.refresh(receiver_user)

        order_draft.receiver_user_id = receiver_user.id
    
    # 6. 若有付款方式（pay_way）等欄位可在此擴充 
    if draft_in.pay_way_id:
        # check if the pay_way is valid
        pay_way = await get_payment_method_by_id(db, draft_in.pay_way_id)
        if not pay_way:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment method with id {draft_in.pay_way_id} not found."
            )
        order_draft.pay_way_id = pay_way.id

    # 7. 提交並 refresh
    db.add(order_draft)
    await db.commit()
    await db.refresh(order_draft)
    
    # 8. 回傳 OrderDraftOut
    return await get_order_draft_by_room_id(db, room_id)