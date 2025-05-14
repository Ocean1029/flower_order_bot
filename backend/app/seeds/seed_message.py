from app.models.chat import ChatRoom, ChatMessage
from datetime import datetime
import random
from faker import Faker

fake = Faker("zh_TW")

async def create_random_message(session, user):
    room = ChatRoom(
        user_id=user.id,
        stage="bot_active",
        bot_step=2,
        unread_count=random.randint(0, 5),
        last_message_ts=datetime.utcnow(),
    )
    session.add(room)
    await session.flush()

    message = ChatMessage(
        room_id=room.id,
        status="sent",
        direction=random.choice(["incoming", "outgoing_by_bot", "outgoing_by_staff"]),
        text=fake.sentence(),
        created_at=datetime.utcnow(),
    )
    session.add(message)
    await session.flush()
    await session.commit()
    
    return room
