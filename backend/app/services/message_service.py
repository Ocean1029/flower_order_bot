from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from datetime import datetime, timezone, timedelta
from typing import List, Optional

from app.models.chat import ChatRoom, ChatMessage
from app.schemas.chat import ChatRoomOut, ChatMessageOut, ChatMessageBase
from app.enums.chat import ChatMessageStatus, ChatRoomStage, ChatMessageDirection
from app.utils.line_send_message import LINE_push_message
from app.services.user_service import get_user_by_line_uid

async def get_latest_message(db: AsyncSession, room_id: int) -> Optional[ChatMessageOut]:
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.room_id == room_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    message = result.scalar_one_or_none()
    return message

async def get_chat_room_list(db: AsyncSession) -> Optional[List[ChatRoomOut]]:
    stmt = (
        select(ChatRoom)
        .options(joinedload(ChatRoom.user))
        .order_by(ChatRoom.updated_at.desc())
    )
    result = await db.execute(stmt)
    rooms = result.scalars().all()

    response = []
    for room in rooms:
        last_msg = await get_latest_message(db, room.id)
        # 如果聊天室沒有訊息，則不顯示最後訊息
        response.append(ChatRoomOut(
            room_id=room.id,
            user_name=room.user.name if room.user else "未知",
            unread_count=room.unread_count,
            status=room.stage,
            last_message={
                "text": last_msg.text if last_msg else None,
                "timestamp": last_msg.created_at if last_msg else None
            } if last_msg else None
        ))

    return response

async def get_chat_room_by_room_id(db: AsyncSession, room_id: int) -> Optional[ChatRoom]:
    stmt = (
        select(ChatRoom)
        .options(joinedload(ChatRoom.user))
        .where(ChatRoom.id == room_id)
    )
    result = await db.execute(stmt)
    room = result.scalar_one_or_none()
    return room

async def get_chat_room_by_user_id(db: AsyncSession, user_id: int) -> Optional[ChatRoom]:
    stmt = (
        select(ChatRoom)
        .options(joinedload(ChatRoom.user))
        .where(ChatRoom.user_id == user_id)
    )
    result = await db.execute(stmt)
    room = result.scalar_one_or_none()
    return room

async def create_chat_room(db: AsyncSession, user_id: int) -> ChatRoom:
    room = ChatRoom(
        user_id=user_id, 
        stage=ChatRoomStage.WELCOME,
        bot_step=-1,
        unread_count=0,
        created_at=datetime.now(timezone(timedelta(hours=8)))
        )
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room

async def get_chat_messages(db: AsyncSession, room_id: int, after: Optional[datetime] = None) -> List[ChatMessageOut]:
    stmt = select(ChatMessage).where(ChatMessage.room_id == room_id)
    if after:
        stmt = stmt.where(ChatMessage.created_at > after)
    stmt = stmt.order_by(ChatMessage.created_at.asc())

    result = await db.execute(stmt)
    messages = result.scalars().all()

    return [
        ChatMessageOut(
            id=message.id,
            direction=message.direction,
            message=ChatMessageBase(
                text=message.text,
                image_url=message.image_url
            ),
            status=message.status,
            created_at=message.created_at
        ) for message in messages
    ]

async def switch_chat_room_mode(db: AsyncSession, room_id: int, mode: str) -> None:
    stmt = (
        update(ChatRoom)
        .where(ChatRoom.id == room_id)
        .values(stage=mode, updated_at=datetime.now(timezone(timedelta(hours=8))))
    )
    await db.execute(stmt)
    await db.commit()

async def create_chat_message_entry(
    db: AsyncSession,
    room_id: int,
    data: ChatMessageBase,
    direction: ChatMessageDirection
) -> ChatMessage:
    message = ChatMessage(
        room_id=room_id,
        direction=direction,
        text=data.text,
        image_url=data.image_url,
        status=ChatMessageStatus.SENT,
        processed=False,
        created_at=datetime.now(timezone(timedelta(hours=8))),
        updated_at=datetime.now(timezone(timedelta(hours=8)))
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message

async def create_staff_message(db: AsyncSession, room_id: int, data: ChatMessageBase) -> ChatMessageOut:
    # 查找聊天室
    room = await get_chat_room_by_room_id(db, room_id)
    if not room:
        raise ValueError("Chat room not found")
    
    # 查找用戶
    user = await get_user_by_line_uid(db, room.user.line_uid)
    if not user:
        raise ValueError("User not found")
    
    # 發送訊息到 LINE
    success = LINE_push_message(user.line_uid, data)
    # if not success:
        # raise ValueError("Failed to send message to LINE")

    # 創建訊息
    message = await create_chat_message_entry(
        db=db,
        room_id=room.id,
        data=data,
        direction=ChatMessageDirection.OUTGOING_BY_STAFF
    )
    
    # 更新聊天室狀態
    room.stage = ChatRoomStage.IDLE
    room.updated_at = datetime.now(timezone(timedelta(hours=8)))
    db.add(room)
    await db.commit()
    await db.refresh(room)

    message_out = ChatMessageOut(
        id=message.id,
        direction=message.direction,
        message=ChatMessageBase(
            text=message.text,
            image_url=message.image_url
        ),
        status=message.status,
        created_at=message.created_at
    )
    return message_out