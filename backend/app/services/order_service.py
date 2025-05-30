# app/services/order_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status

from app.models.user import User
from app.models.order import Order, OrderDraft

from app.models.chat import ChatRoom, ChatMessage
from app.schemas.order import OrderOut, OrderDraftOut, OrderDraftUpdate, OrderCreate
from app.services.payment_service import get_pay_way_by_order_id, get_payment_method_by_id
from app.services.user_service import get_user_by_id, update_user_info, get_line_uid_by_chatroom_id
from app.services.message_service import get_chat_room_by_room_id
from app.enums.order import OrderStatus
from app.enums.shipment import ShipmentStatus
from app.enums.chat import ChatMessageStatus, ChatRoomStage, ChatMessageDirection
from app.utils.line_send_message import LINE_push_message
from app.schemas.chat import ChatMessageBase

async def get_order(db: AsyncSession, order_id: int) -> Order:
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_all_orders(db: AsyncSession) -> Optional[List[OrderOut]]:
    results = []

    # 撈出所有訂單
    order_stmt = select(Order).where(Order.status != OrderStatus.CANCELLED)
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
            
            pay_way=pay_way.display_name if pay_way else None,
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

    # 依照 id descending 排序
    results.sort(key=lambda x: x.id, reverse=True)
    return results

async def validate_order_draft_required_fields(db, order_draft: OrderDraft) -> tuple[bool, list[str]]:
    """
    檢查訂單草稿的必要欄位是否完整
    回傳: (是否完整, 缺少的欄位列表)
    """
    if not order_draft:
        return False, ["order_draft"]
    
    # 定義必要欄位
    required_fields = [
        "user_id",
        "receiver_user_id",
        "item_type",
        "quantity",
        "total_amount",
        "shipment_method",
    ]
    
    missing_fields = []
    for field in required_fields:
        if not getattr(order_draft, field):
            missing_fields.append(field)
    
    # 檢查 user 的 name 和 phone
    user = await get_user_by_id(db, order_draft.user_id)
    if not user:
        missing_fields.append("user")
    elif not user.name:
        missing_fields.append("user_name")
    elif not user.phone:
        missing_fields.append("user_phone")
    
    receiver_user = await get_user_by_id(db, order_draft.receiver_user_id)
    if not receiver_user:
        missing_fields.append("receiver")
    elif not receiver_user.name:
        missing_fields.append("receiver_name")
    elif not receiver_user.phone:
        missing_fields.append("receiver_phone")

    return len(missing_fields) == 0, missing_fields

async def create_order_by_room(db: AsyncSession, room_id: int) -> list[str]:
    room = await get_chat_room_by_room_id(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat room with id {room_id} not found."
        )
    
    order_draft = await get_order_draft_by_room(db, room_id)
    if not order_draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order draft for room {room_id} not found."
        )
    
    is_complete, missing_fields = await validate_order_draft_required_fields(db, order_draft)
    if not is_complete:
        return missing_fields

    order = Order(
        room_id=order_draft.room_id,
        user_id=order_draft.user_id,
        receiver_user_id=order_draft.receiver_user_id,
        status=OrderStatus.CONFIRMED,
        item_type=order_draft.item_type,
        quantity=order_draft.quantity,
        total_amount=order_draft.total_amount,
        notes=order_draft.notes,
        card_message=order_draft.card_message,
        shipment_method=order_draft.shipment_method,
        shipment_status=ShipmentStatus.PENDING,
        receipt_address=order_draft.receipt_address,
        delivery_address=order_draft.delivery_address,
        delivery_datetime=order_draft.delivery_datetime,
        created_at=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None),
        updated_at=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)
    )
    
    db.add(order)
    await db.commit()
    await db.refresh(order)

    # 更新聊天室的 stage
    room.stage = ChatRoomStage.ORDER_CONFIRM
    await db.commit()
    await db.refresh(room)
    print("聊天室，已設定成「訂單確認」模式")

   # 透過 room_id 反查目前聊天室對應的 LINE UID
    line_uid = await get_line_uid_by_chatroom_id(db, room.id)
    msg = f"訂單已經由後台送出囉～\n\n"
    if not line_uid:
        print("❗ 無法取得 LINE UID，無法推播訂單已送出提醒。")
    LINE_push_message(line_uid, ChatMessageBase(text=msg))
    print("已傳送訊息: ", msg)
    
    # 儲存提醒訊息的動作
    message = ChatMessage(
        room_id=room.id,
        direction=ChatMessageDirection.OUTGOING_BY_BOT,
        text="[自動回覆已傳送]" + msg,
        image_url="",
        status=ChatMessageStatus.PENDING,
        processed=True, 
        created_at=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None),
        updated_at=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)
        )
    db.add(message)
    await db.commit()
    
    return []

async def update_order_by_room_id(
    db: AsyncSession,
    room_id: int,
) -> bool:
    """
    更新指定房間最新一筆已確認的訂單
    """
    # 1. 取得聊天室
    room = await get_chat_room_by_room_id(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat room with id {room_id} not found."
        )

    # 2. 取得 order draft
    order_draft = await get_order_draft_by_room(db, room_id)
    if not order_draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order draft for room {room_id} not found."
        )
    
    # 2.5 validate order_draft
    is_complete = await validate_order_draft_required_fields(db, order_draft)
    if not is_complete[0]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"訂單草稿不完整，缺少以下欄位：{', '.join(is_complete[1])}"
        )

    # 3. 取得最新的訂單
    stmt = (
        select(Order)
        .where(Order.room_id == room.id, Order.status == OrderStatus.CONFIRMED)
        .order_by(Order.created_at.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No confirmed order found for room {room_id}."
        )

    # 3. 依據 OrderDraft 的資料更新最新一筆 Order
    
    order.user_id = order_draft.user_id
    order.receiver_user_id = order_draft.receiver_user_id
    order.item_type = order_draft.item_type
    order.quantity = order_draft.quantity
    order.total_amount = order_draft.total_amount
    order.notes = order_draft.notes
    order.card_message = order_draft.card_message
    order.shipment_method = order_draft.shipment_method
    order.receipt_address = order_draft.receipt_address
    order.delivery_address = order_draft.delivery_address
    order.delivery_datetime = order_draft.delivery_datetime
    order.updated_at = datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)


    # 4. 提交並 refresh
    db.add(order)
    await db.commit()
    await db.refresh(order)

    return True

async def delete_order_by_id(db: AsyncSession, order_id: int) -> bool:
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found."
        )
    
    order.status = OrderStatus.CANCELLED
    await db.commit()
    await db.refresh(order)
    return True
    
async def get_order_draft_by_room(db: AsyncSession, room_id: int) -> Optional[OrderDraft]:
    stmt = (
        select(OrderDraft)
        .where(OrderDraft.room_id == room_id)
        .order_by(OrderDraft.created_at.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    order_draft = result.scalar_one_or_none()
    
    return order_draft

async def get_order_draft_out_by_room(db: AsyncSession, room_id: int) -> Optional[OrderDraftOut]:
    stmt = (
        select(OrderDraft)
        .where(OrderDraft.room_id == room_id)
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
            
            pay_way=pay_way.display_name if pay_way else None, 
            total_amount=order_draft.total_amount,
            
            item=order_draft.item_type,
            quantity=order_draft.quantity,
            note=order_draft.notes,
            card_message=order_draft.card_message,
            
            shipment_method=order_draft.shipment_method,
            weekday=order_draft.created_at.strftime("%A"),
            send_datetime=order_draft.delivery_datetime or None, # 這裡指的是取貨時間
            receipt_address=order_draft.receipt_address,
            delivery_address=order_draft.delivery_address or order_draft.receipt_address or ""
        )
    
    return None

async def create_order_draft_by_room_id(
    db: AsyncSession,
    room_id: int,
) -> OrderDraft:
    """
    依據 room_id 新建一筆 order_draft
    -----------------------------------------------------------------
    - 若 room_id 查無聊天室 → 404
      若該 room 中已有草稿 -> 400
    - 回傳 *OrderDraft ORM*，呼叫端可再轉成 Pydantic
    """

    # 1. 取得聊天室
    room = await get_chat_room_by_room_id(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat room with id {room_id} not found."
        )

    order_draft = await get_order_draft_by_room(db, room_id)
    if order_draft:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order draft for room {room_id} already exists."
        )
    
    order_draft = OrderDraft(
        room_id=room.id,
        user_id=room.user_id,
        receiver_user_id=room.user_id,
        created_at=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None),
        updated_at=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)
    )
    db.add(order_draft)
    await db.commit()
    await db.refresh(order_draft)

    return order_draft

async def update_order_draft_by_room_id(
    db: AsyncSession, room_id: int, draft_in: OrderDraftUpdate
) -> OrderDraftOut:
    room = await get_chat_room_by_room_id(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat room with id {room_id} not found."
        )

    order_draft = await get_order_draft_by_room(db, room_id)
    if not order_draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order draft with room id {room_id} not found."
        )
    
    if draft_in.customer_name is not None or draft_in.customer_phone is not None:
        user = await get_user_by_id(db, order_draft.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {order_draft.user_id} not found."
            )
        user = await update_user_info(
            db,
            user.id,
            name=draft_in.customer_name or user.name,
            phone=draft_in.customer_phone or user.phone
        )

    # 5. 新增收件人資訊
    if draft_in.receiver_name or draft_in.receiver_phone:
        # just create the receiver user directly, TODO: Add a "order relation" table to store the relation between the customer and receiver
        receiver_user = User(
            name=draft_in.receiver_name,
            phone=draft_in.receiver_phone,
            created_at=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None),
            updated_at=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None),
        )
        db.add(receiver_user)
        await db.commit()
        await db.refresh(receiver_user)

        order_draft.receiver_user_id = receiver_user.id
    
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
        # 把 send_datetime 轉成 UTC +8
        order_draft.delivery_datetime = draft_in.send_datetime.astimezone(timezone(timedelta(hours=8))).replace(tzinfo=None)
    if draft_in.receipt_address is not None:
        order_draft.receipt_address = draft_in.receipt_address
    if draft_in.delivery_address is not None:
        order_draft.delivery_address = draft_in.delivery_address
    order_draft.updated_at = datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)

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
    return await get_order_draft_out_by_room(db, room_id)
