from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.chat import ChatRoom
from typing import Optional

from app.schemas.user import UserCreate


async def get_line_uid_by_chatroom_id(
        db: AsyncSession,
        chat_room_id: int
    ) -> Optional[str]:
    """
    Given a chat_room_id, return the associated user's LINE UID.

    Args:
        db (AsyncSession): SQLAlchemy async session.
        chat_room_id (int): Primary key of the ChatRoom record.

    Returns:
        Optional[str]: LINE UID if the chat room exists and has one, else None.
    """
    user = await get_user_by_chat_room_id(db, chat_room_id)
    if user and user.line_uid:
        return user.line_uid


async def get_user_by_line_uid(db: AsyncSession, line_uid: str) -> User:
    stmt = select(User).where(User.line_uid == line_uid)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_chat_room_id(
        db: AsyncSession, 
        chat_room_id: int
    ) -> Optional[User]:
    """
    Given a chat_room_id, return the associated User.

    Args:
        db (AsyncSession): SQLAlchemy async session.
        chat_room_id (int): Primary key of the ChatRoom record.

    Returns:
        Optional[User]: User object if found, else None.
    """
    chat_room = await db.execute(
        select(ChatRoom).
        options(selectinload(ChatRoom.user)).
        where(ChatRoom.id == chat_room_id)
    )
    chat_room = chat_room.scalar_one_or_none()

    if not chat_room:
        raise Exception("Chat room not found")

    return chat_room.user

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
    user.updated_at = datetime.now(timezone(timedelta(hours=8)))
    await db.commit()
    await db.refresh(user)
    return user