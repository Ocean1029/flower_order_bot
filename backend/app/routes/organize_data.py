# backend/app/routes/organize_data.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.order import OrderDraftOut
from app.services.organize_data import organize_data
from fastapi import HTTPException, status

api_router = APIRouter(prefix="/organize_data", tags=["Organize Data"])

@api_router.post("/organize_data/{room_id}", response_model=OrderDraftOut)
async def organize_data_by_room_id(
    room_id: int,
    db: AsyncSession = Depends(get_db)
):
    organize_data_result = await organize_data(db, room_id)
    if not organize_data_result:
        raise HTTPException(status_code=404, detail="No data found")
    return organize_data_result