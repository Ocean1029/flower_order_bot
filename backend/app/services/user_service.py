from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.chat import ChatRoom


async def get_user_by_line_uid(db: AsyncSession, line_uid: str) -> User:
    stmt = select(User).where(User.line_uid == line_uid)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, line_uid: str, name: str) -> User:
    user = User(line_uid=line_uid, name=name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

