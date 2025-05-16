from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.payment_service import get_all_payment_methods
from app.schemas.payment import PaymentMethodBase
    
api_router = APIRouter(tags=["Payment"])

@api_router.get("/payment_methods", response_model=list[PaymentMethodBase])
async def get_payment_methods(db: AsyncSession = Depends(get_db)):
    return await get_all_payment_methods(db)

