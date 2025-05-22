from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.chat import ChatRoom
from typing import Optional

from app.schemas.user import UserCreate


async def get_user_by_line_uid(db: AsyncSession, line_uid: str) -> User:
    stmt = select(User).where(User.line_uid == line_uid)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(
        db: AsyncSession, 
        user_data: UserCreate
        ) -> User:
    user = User(**user_data.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_info(
                db: AsyncSession,
                user_id: int,
                name: Optional[str] = None,
                phone: Optional[str] = None,
            ) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise Exception("User not found")
    if name:
        user.name = name
    if phone:
        user.phone = phone
    user.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    return user