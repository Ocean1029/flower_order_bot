from core.database import SessionLocal
from models.chat import ChatMessage, ChatRoom
from models.user import User
from sqlalchemy import func, desc

def get_latest_messages():
    session = SessionLocal()

    subquery = session.query(
        ChatMessage.room_id,
        func.max(ChatMessage.created_at).label("latest_time")
    ).group_by(ChatMessage.room_id).subquery()

    latest_messages = session.query(ChatMessage).join(
        subquery,
        (ChatMessage.room_id == subquery.c.room_id) &
        (ChatMessage.created_at == subquery.c.latest_time)
    ).order_by(desc(ChatMessage.created_at)).all()

    result = []
    for msg in latest_messages:
        room = session.query(ChatRoom).filter_by(id=msg.room_id).first()
        user = session.query(User).filter_by(id=room.user_id).first() if room else None

        result.append({
            "id": msg.id,
            "customer_name": user.name if user else "(未知用戶)",
            "phone": user.phone if user else "(無電話)",
            "preview": msg.text[:40],
            "time": msg.created_at.strftime("%Y-%m-%d %H:%M")
        })

    session.close()
    return result
