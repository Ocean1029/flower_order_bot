from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import csv
from io import StringIO
from typing import List, Optional

from app.services.order_service import get_all_orders, get_order_draft_by_room_id, update_order_draft_by_id
from app.core.database import get_db
from app.schemas.order import OrderOut, OrderDraftOut, OrderDraftUpdate

api_router = APIRouter()

@api_router.get("/orders", response_model=Optional[List[OrderOut]])
async def get_orders(db: AsyncSession = Depends(get_db)):
    return await get_all_orders(db)

@api_router.get("/orderdraft/{room_id}", response_model=Optional[OrderDraftOut])
async def get_order_draft(room_id: int, db: AsyncSession = Depends(get_db)):
    return await get_order_draft_by_room_id(db, room_id)


@api_router.patch("/orderdraft/{room_id}", response_model=Optional[OrderDraftOut])
async def update_order_draft(room_id: int, order_draft: OrderDraftUpdate, db: AsyncSession = Depends(get_db)):
    return await update_order_draft_by_id(db, room_id, order_draft)


# @api_router.get("/orders.csv")
# async def export_orders_csv(db: AsyncSession = Depends(get_db)):
#     """
#     下載訂單資料為 CSV 檔案
#     """
#     data = await get_all_orders(db)

#     output = []
#     output.append([
#         "訂單ID", "姓名", "電話", "花材", "數量", "預算", "取貨方式", "取貨日期", "取貨時間", "備註"
#     ])

#     for o in data:
#         output.append([
#             o["id"],
#             o["customer_name"],
#             o["phone"],
#             o["flower"],
#             o["qty"],
#             o["budget"],
#             o["pickup_method"],
#             o["pickup_date"],
#             o["pickup_time"],
#             o["note"],
#         ])
    
#     # 創建 CSV 字串
#     csv_file = StringIO()
#     writer = csv.writer(csv_file)
#     writer.writerows(output)
    
#     # 重置檔案指針
#     csv_file.seek(0)
    
#     return StreamingResponse(
#         iter([csv_file.getvalue()]),
#         media_type="text/csv",
#         headers={"Content-Disposition": "attachment; filename=orders.csv"}
#     )

