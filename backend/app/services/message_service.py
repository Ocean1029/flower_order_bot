# backend/app/services/chat.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from datetime import datetime
from typing import List, Optional
from app.models.chat import ChatRoom, ChatMessage
from app.models.user import User
from app.schemas.chat import ChatRoomOut, ChatMessageOut, ChatMessageCreate
from app.utils.line import LINE_push_message


async def get_chat_room_list(db: AsyncSession) -> List[ChatRoomOut]:
    stmt = (
        select(ChatRoom)
        .options(joinedload(ChatRoom.user))
        .order_by(ChatRoom.updated_at.desc())
    )
    result = await db.execute(stmt)
    rooms = result.scalars().all()

    response = []
    for room in rooms:
        # 查找最後一則訊息
        msg_stmt = (
            select(ChatMessage)
            .where(ChatMessage.room_id == room.id)
            .order_by(ChatMessage.created_at.desc())
            .limit(1)
        )
        msg_result = await db.execute(msg_stmt)
        last_msg = msg_result.scalar_one_or_none()

        response.append(ChatRoomOut(
            room_id=room.id,
            user_name=room.user.name if room.user else "未知",
            unread_count=room.unread_count,
            status=room.stage,
            last_message={
                "text": last_msg.text if last_msg else "",
                "timestamp": last_msg.created_at if last_msg else None
            } if last_msg else None
        ))

    return response


async def get_chat_messages(db: AsyncSession, room_id: int, after: Optional[datetime] = None) -> List[ChatMessageOut]:
    stmt = select(ChatMessage).where(ChatMessage.room_id == room_id)
    if after:
        stmt = stmt.where(ChatMessage.created_at > after)
    stmt = stmt.order_by(ChatMessage.created_at.asc())

    result = await db.execute(stmt)
    messages = result.scalars().all()

    return [
        ChatMessageOut(
            id=m.id,
            direction=m.direction,
            text=m.text,
            image_url=m.image_url,
            status=m.status,
            line_msg_id=m.line_msg_id,
            processed=m.processed,
            created_at=m.created_at
        ) for m in messages
    ]


async def switch_chat_room_mode(db: AsyncSession, room_id: int, mode: str) -> None:
    stmt = (
        update(ChatRoom)
        .where(ChatRoom.id == room_id)
        .values(stage=mode, updated_at=datetime.utcnow())
    )
    await db.execute(stmt)
    await db.commit()


async def create_staff_message(db: AsyncSession, room_id: int, data: ChatMessageCreate) -> ChatMessage:
    # 取得聊天室與顧客
    stmt = select(ChatRoom).where(ChatRoom.id == room_id)
    room_result = await db.execute(stmt)
    room = room_result.scalar_one_or_none()
    if not room:
        raise ValueError("Chat room not found")

    user_stmt = select(User).where(User.id == room.user_id)
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()
    if not user or not user.line_uid:
        raise ValueError("User LINE ID not found")

    # 發送訊息到 LINE
    success = LINE_push_message(user.line_uid, data)
    # if not success:
        # raise ValueError("Failed to send message to LINE")

    # 寫入訊息紀錄
    message = ChatMessage(
        room_id=room_id,
        direction="outgoing_by_staff",
        text=data.text,
        image_url=data.image_url,
        status="sent",
        processed=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(message)


    await db.commit()
    await db.refresh(message)
    return message
