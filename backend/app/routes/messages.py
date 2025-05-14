# backend/app/routes/chat.py

from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.chat import ChatRoomOut, ChatRoomModeSwitch
from app.schemas.chat import ChatMessageOut, ChatMessageCreate
from app.services.message_service import (
    get_chat_room_list,
    get_chat_messages,
    create_staff_message,
    switch_chat_room_mode
)

api_router = APIRouter(prefix="/chat_rooms", tags=["Chat"])

@api_router.get("", response_model=List[ChatRoomOut])
async def list_chat_rooms(db: AsyncSession = Depends(get_db)):
    return await get_chat_room_list(db)


@api_router.get("/{room_id}/messages", response_model=List[ChatMessageOut])
async def get_messages(
    room_id: int,
    after: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    return await get_chat_messages(db, room_id, after=after)


@api_router.post("/{room_id}/messages")
async def post_message(room_id: int, message: ChatMessageCreate, db: AsyncSession = Depends(get_db)):
    result = await create_staff_message(db, room_id, message)
    return {"status": "ok", "message_id": result.id}

@api_router.post("/{room_id}/switch_mode")
async def switch_mode(room_id: int, body: ChatRoomModeSwitch, db: AsyncSession = Depends(get_db)):
    await switch_chat_room_mode(db, room_id, body.mode)
    return {"status": "ok", "new_mode": body.mode}