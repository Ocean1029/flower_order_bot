from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.order_service import get_all_orders
from app.core.database import get_db
import csv
from typing import List
from io import StringIO
from app.schemas.order import OrderOut

api_router = APIRouter()

@api_router.get("/orders", response_model=List[OrderOut])
async def get_orders(db: AsyncSession = Depends(get_db)):
    return await get_all_orders(db)


@api_router.get("/orders.csv")
async def export_orders_csv(db: AsyncSession = Depends(get_db)):
    """
    下載訂單資料為 CSV 檔案
    """
    data = await get_all_orders(db)

    output = []
    output.append([
        "訂單ID", "姓名", "電話", "花材", "數量", "預算", "取貨方式", "取貨日期", "取貨時間", "備註"
    ])

    for o in data:
        output.append([
            o["id"],
            o["customer_name"],
            o["phone"],
            o["flower"],
            o["qty"],
            o["budget"],
            o["pickup_method"],
            o["pickup_date"],
            o["pickup_time"],
            o["note"],
        ])
    
    # 創建 CSV 字串
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    writer.writerows(output)
    
    # 重置檔案指針
    csv_file.seek(0)
    
    return StreamingResponse(
        iter([csv_file.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=orders.csv"}
    )

