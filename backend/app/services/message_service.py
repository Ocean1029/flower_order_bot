from app.models.chat import ChatMessage, ChatRoom
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, desc, select
from typing import List, Dict

async def get_latest_messages(session: AsyncSession) -> List[Dict]:
    # Step 1: 子查詢，每個聊天室的最新訊息時間
    subquery = (
        select(
            ChatMessage.room_id,
            func.max(ChatMessage.created_at).label("latest_time")
        )
        .group_by(ChatMessage.room_id)
        .subquery()
    )

    # Step 2: JOIN ChatMessage, ChatRoom, User + subquery
    stmt = (
        select(ChatMessage, ChatRoom, User)
        .join(ChatRoom, ChatMessage.room_id == ChatRoom.id)
        .join(User, ChatRoom.user_id == User.id)
        .join(
            subquery,
            (ChatMessage.room_id == subquery.c.room_id) &
            (ChatMessage.created_at == subquery.c.latest_time)
        )
        .order_by(desc(ChatMessage.created_at))
    )

    result = []
    rows = await session.execute(stmt)

    for msg, room, user in rows.all():
        result.append({
            "id": msg.id,
            "customer_name": user.name,
            "phone": user.phone,
            "preview": msg.text[:40],
            "time": msg.created_at.strftime("%Y-%m-%d %H:%M")
        })

    return result
