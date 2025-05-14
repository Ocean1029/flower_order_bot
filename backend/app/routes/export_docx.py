from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.order_service import get_all_orders
from app.core.database import get_db
from docx import Document
import io
import os

api_router = APIRouter()

TEMPLATE_PATH = "order_template.docx"

def fill_placeholders(paragraphs, data):
    for para in paragraphs:
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in para.text:
                para.text = para.text.replace(placeholder, str(value or ""))
    return paragraphs

@api_router.get("/orders.docx")
async def export_orders_docx(db: AsyncSession = Depends(get_db)):
    orders = await get_all_orders(db)

    # 資料轉為 dict（保險）
    order_dicts = [order.dict() if hasattr(order, 'dict') else order for order in orders]

    combined_doc = Document()

    for order in order_dicts:
        # 你可以在這裡對 order 做欄位映射轉換
        mapped_data = {
            "id": order["id"],
            "customer_name": order["customer_name"],
            "phone": order["customer_phone"],
            "timestamp": order.get("order_date", "").strftime("%Y-%m-%d") if order.get("order_date") else "",            "收據寄送地址": order.get("receipt_address", ""),
            "ITEM": order["item"],
            "QTY": order["quantity"],
            "PAY WAY": order.get("payway", ""),
            "備註": order["note"],
            "卡片內容：（範例請看圖）": order.get("card_message", ""),
            "星期": order.get("weekday", ""),
            "SEND DAY & TIME": order.get("send_datetime", ""),
            "RECEIVER NAME": order.get("receiver_name", ""),
            "MOBILE": order.get("receiver_phone", ""),
            "ADD": order.get("delivery_address", "")
        }

        # 載入模板
        template_doc = Document(TEMPLATE_PATH)
        fill_placeholders(template_doc.paragraphs, mapped_data)
        for element in template_doc.element.body:
            combined_doc.element.body.append(element)
        combined_doc.add_page_break()

    # 儲存至記憶體
    file_stream = io.BytesIO()
    combined_doc.save(file_stream)
    file_stream.seek(0)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=flower_orders.docx"}
    )
