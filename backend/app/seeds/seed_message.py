from app.models.chat import ChatRoom, ChatMessage
from datetime import datetime, timedelta
import random
from faker import Faker
from app.enums.chat import ChatRoomStage, ChatMessageStatus, ChatMessageDirection

fake = Faker("zh_TW")

async def create_random_message(session, user):
    # 創建聊天室
    room = ChatRoom(
        user_id=user.id,
        stage=ChatRoomStage.BOT_ACTIVE,
        bot_step=random.randint(1, 5),
        unread_count=random.randint(0, 5),
        last_message_ts=datetime.utcnow(),
    )
    session.add(room)
    await session.flush()

    # 創建多條訊息來模擬對話
    messages = []
    base_time = datetime.utcnow() - timedelta(hours=random.randint(1, 24))
    
    # 第一條訊息一定是機器人的歡迎訊息
    welcome_message = ChatMessage(
        room_id=room.id,
        status=ChatMessageStatus.SENT,
        direction=ChatMessageDirection.OUTGOING_BY_BOT,
        text="您好！歡迎使用我們的訂花服務，請問有什麼可以協助您的嗎？",
        created_at=base_time,
    )
    messages.append(welcome_message)
    
    # 隨機生成 3-7 條訊息
    for i in range(random.randint(3, 7)):
        message_time = base_time + timedelta(minutes=random.randint(5, 30))
        direction = random.choice([
            ChatMessageDirection.INCOMING,
            ChatMessageDirection.OUTGOING_BY_BOT,
            ChatMessageDirection.OUTGOING_BY_STAFF
        ])
        
        # 根據訊息方向生成不同的內容
        if direction == ChatMessageDirection.INCOMING:
            text = fake.sentence()
        elif direction == ChatMessageDirection.OUTGOING_BY_BOT:
            text = random.choice([
                "好的，我了解您的需求。",
                "請問您想要什麼樣的花束呢？",
                "我們有提供多種花束選擇，您想要哪一種呢？",
                "請問您需要什麼時候送達呢？",
                "好的，我已經記錄下來了。"
            ])
        else:  # OUTGOING_BY_STAFF
            text = random.choice([
                "您好，我是客服人員，很高興為您服務。",
                "您的訂單已經確認了。",
                "我們會盡快處理您的訂單。",
                "請問還有其他需要協助的嗎？",
                "感謝您的訂購！"
            ])
        
        message = ChatMessage(
            room_id=room.id,
            status=ChatMessageStatus.SENT,
            direction=direction,
            text=text,
            created_at=message_time,
        )
        messages.append(message)
        base_time = message_time
    
    # 更新最後訊息時間
    room.last_message_ts = base_time
    
    # 批量添加訊息
    for message in messages:
        session.add(message)
    
    await session.flush()
    await session.commit()
    
    return room
