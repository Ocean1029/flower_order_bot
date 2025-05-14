import random
from faker import Faker
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

fake = Faker("zh_TW")

async def create_random_user(session: AsyncSession) -> User:
    user = User(
        line_uid=fake.uuid4(),
        name=fake.name(),
        phone=fake.phone_number(),
        has_ordered=False,
    )
    session.add(user)
    await session.flush()  # 讓 user 拿到 id
    return user
