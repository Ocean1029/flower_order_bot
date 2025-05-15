import asyncio
from app.seeds.seed_user import create_random_user
from app.seeds.seed_order import create_random_order
from app.seeds.seed_message import create_random_message
from app.core.database import get_db

async def main():
    async for session in get_db():
        await seed_test_data(session)
        print("✅ 測試資料產生完畢")    

async def seed_test_data(session, count: int = 10):
    for _ in range(count):
        user = await create_random_user(session)
        room = await create_random_message(session, user)
        await create_random_order(session, user)
        
    await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
