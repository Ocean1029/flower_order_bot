from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.order_service import get_all_orders
from app.core.database import get_db
from docxtpl import DocxTemplate
import io

api_router = APIRouter()
TEMPLATE_PATH = "order_template.docx"

@api_router.get("/orders/{order_id}.docx")
async def export_order_docx(order_id: int, db: AsyncSession = Depends(get_db)):
    orders = await get_all_orders(db)
    order = next((o for o in orders if o.id == order_id), None)
    if not order:
        return {"error": "Order not found"}

    # 處理 send_datetime 與中文星期
    send_datetime_str = ""
    weekday_str = ""
    if getattr(order, "send_datetime", None):
        send_datetime_str = order.send_datetime.strftime("%Y-%m-%d %H:%M")
        WEEKDAY_MAP = {
            "Monday": "星期一",
            "Tuesday": "星期二",
            "Wednesday": "星期三",
            "Thursday": "星期四",
            "Friday": "星期五",
            "Saturday": "星期六",
            "Sunday": "星期日",
        }
        weekday_str = WEEKDAY_MAP.get(order.send_datetime.strftime("%A"), "")

    context = {
        "customer_name": order.customer_name,
        "phone": order.customer_phone,
        "timestamp": order.order_date.strftime("%Y-%m-%d") if getattr(order, "order_date", None) else "",
        "receipt_address": getattr(order, "receipt_address", ""),
        "item": order.item,
        "quantity": order.quantity,
        "pay_way": getattr(order, "pay_way", ""),
        "note": order.note,
        "card_message": getattr(order, "card_message", ""),
        "weekday": weekday_str,
        "send_datetime": send_datetime_str,
        "receiver_name": getattr(order, "receiver_name", ""),
        "receiver_phone": getattr(order, "receiver_phone", ""),
        "delivery_address": getattr(order, "delivery_address", ""),
        "total_amount": getattr(order, "total_amount", 0),
    }

    tpl = DocxTemplate(TEMPLATE_PATH)
    tpl.render(context)

    file_stream = io.BytesIO()
    tpl.save(file_stream)
    file_stream.seek(0)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=order_{order_id}.docx"}
    )
