from core.database import SessionLocal
from models.message import Message
from models.user import User
from sqlalchemy import func, desc

def get_latest_messages():
    session = SessionLocal()

    subquery = session.query(
        Message.user_id,
        func.max(Message.timestamp).label("latest_time")
    ).group_by(Message.user_id).subquery()

    latest_messages = session.query(Message).join(
        subquery,
        (Message.user_id == subquery.c.user_id) &
        (Message.timestamp == subquery.c.latest_time)
    ).order_by(desc(Message.timestamp)).all()

    result = []
    for msg in latest_messages:
        user = session.query(User).filter_by(line_id=msg.user_id).first()
        result.append({
            "id": msg.id,
            "customer_name": user.customer_name if user else "",
            "phone": user.phone_number if user else "",
            "preview": msg.text[:40],
            "time": msg.timestamp.strftime("%Y-%m-%d %H:%M")
        })
    session.close()
    return result
