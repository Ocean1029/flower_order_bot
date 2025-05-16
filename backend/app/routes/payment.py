from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.payment_service import get_all_payment_methods, toggle_payment_method_active, get_payment_method_by_id
from app.schemas.payment import PaymentMethodBase
    
api_router = APIRouter(tags=["Payment"])

@api_router.get("/payment_methods", response_model=list[PaymentMethodBase])
async def get_payment_methods(db: AsyncSession = Depends(get_db)):
    return await get_all_payment_methods(db)

@api_router.patch("/payment_methods/{payment_method_id}", response_model=PaymentMethodBase)
async def toggle_payment_method(payment_method_id: int, db: AsyncSession = Depends(get_db)):
    return await toggle_payment_method_active(db, payment_method_id)

@api_router.get("/payment_methods/{payment_method_id}", response_model=PaymentMethodBase)
async def get_payment_method(payment_method_id: int, db: AsyncSession = Depends(get_db)):
    payment_method = await get_payment_method_by_id(db, payment_method_id)
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment method not found")
    return payment_method