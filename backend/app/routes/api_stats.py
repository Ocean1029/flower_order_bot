from fastapi import APIRouter, Depends
from typing import List
from app.schemas.schema import Stat
from app.services.stats_service import get_stats

api_router = APIRouter(tags=["Dashboard"])

@api_router.get("/api/stats", response_model=List[Stat])
async def stats_api():
    return get_stats()
