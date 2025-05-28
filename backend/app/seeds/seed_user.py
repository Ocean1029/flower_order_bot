import random
from faker import Faker
from app.models.user import User
from app.models.chat import ChatRoom
from app.models.order import OrderDraft
from app.enums.order import OrderDraftStatus
from app.enums.shipment import ShipmentMethod, ShipmentStatus
from app.enums.chat import ChatRoomStage
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

fake = Faker("zh_TW")

async def create_id_prefix(session, serial_number) -> str:
    """Create a prefix based on the current date in yymmddMMM format."""
    id_prefix = datetime.now().strftime("%y%m%d")
    id = f"{id_prefix}{serial_number:03d}"
    return id

async def create_random_user(session: AsyncSession, serial_number) -> User:
    id = await create_id_prefix(session, serial_number)
    avatar_url = fake.image_url(width=200, height=200)

    user = User(
        id=id,
        line_uid=fake.uuid4(),
        name=fake.name(),
        phone=fake.phone_number(),
        has_ordered=False,
        avatar_url=avatar_url,
    )
    session.add(user)
    await session.flush()

    room = ChatRoom(
        user_id=user.id,
        stage=ChatRoomStage.WELCOME,
        bot_step=-1,
        unread_count=random.randint(0, 5),
        last_message_ts=datetime.now(timezone(timedelta(hours=8))),
    )

    session.add(room)
    await session.flush()

    draft = OrderDraft(
        room_id=room.id,
        user_id=user.id,
        receiver_user_id=user.id,  # 預設收件人就是訂購人
    )
    session.add(draft)
    await session.flush()
    return user, room


