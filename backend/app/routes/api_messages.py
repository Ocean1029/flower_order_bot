from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.message_service import get_latest_messages
from app.core.database import get_db

api_router = APIRouter()

@api_router.get("/api/messages")
async def get_messages(db: AsyncSession = Depends(get_db)):
    messages = await get_latest_messages(db)
    return JSONResponse(content={"messages": messages})
