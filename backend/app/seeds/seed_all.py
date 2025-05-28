import asyncio
from app.seeds.seed_user import create_random_user
from app.seeds.seed_order import create_random_order
from app.seeds.seed_message import create_random_message
from app.core.database import get_db

# 流水號
serial_number = 0

async def generate_fake_data(count: int = 10):
    global serial_number
    async for session in get_db():
        await seed_test_data(session, count)
        serial_number += count
        print("✅ 測試資料產生完畢")    

async def seed_test_data(session, count):
    for i in range(count):
        user, room = await create_random_user(session, serial_number + i + 1)
        await create_random_message(session, room)
        await create_random_order(session, user, serial_number + i + 1)
        
    await session.commit()

if __name__ == "__main__":
    asyncio.run(generate_fake_data())
