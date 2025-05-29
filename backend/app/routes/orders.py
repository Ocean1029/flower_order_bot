from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.services.order_service import get_all_orders, get_order_draft_out_by_room, update_order_draft_by_room_id, delete_order_by_id, create_order_by_room
from app.core.database import get_db
from app.schemas.order import OrderOut, OrderDraftOut, OrderDraftUpdate, OrderDraftCreate
api_router = APIRouter()

@api_router.get("/orders", response_model=Optional[List[OrderOut]])
async def get_orders(db: AsyncSession = Depends(get_db)):
    return await get_all_orders(db)

# 刪除 order
@api_router.delete("/order/{order_id}", response_model=bool)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_order_by_id(db, order_id)

# 新增 order
@api_router.post("/order/{room_id}", response_model=bool)
async def create_order(room_id: int, db: AsyncSession = Depends(get_db)):
    return await create_order_by_room(db, room_id)

@api_router.get("/orderdraft/{room_id}", response_model=Optional[OrderDraftOut])
async def get_order_draft(room_id: int, db: AsyncSession = Depends(get_db)):
    return await get_order_draft_out_by_room(db, room_id)

@api_router.patch("/orderdraft/{room_id}", response_model=Optional[OrderDraftOut])
async def update_order_draft(room_id: int, order_draft: OrderDraftUpdate, db: AsyncSession = Depends(get_db)):
    return await update_order_draft_by_room_id(db, room_id, order_draft)

# @api_router.post("/orderdraft/{room_id}", response_model=Optional[OrderDraftOut])
# async def create_order_draft(room_id: int, order_draft: OrderDraftCreate, db: AsyncSession = Depends(get_db)):
#     return await create_order_draft_by_room_id(db, room_id, order_draft)

