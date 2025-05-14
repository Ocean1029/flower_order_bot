from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.stats import StatsOut
from app.services.stats_service import get_stats

api_router = APIRouter(tags=["Dashboard"])

@api_router.get("/api/stats", response_model=StatsOut)
async def stats_api(db: AsyncSession = Depends(get_db)):
    return await get_stats(db)
