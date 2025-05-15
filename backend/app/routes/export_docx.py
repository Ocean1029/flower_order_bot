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

    context = {
        "customer_name": order.customer_name,
        "phone": order.customer_phone,
        "timestamp": order.order_date.strftime("%Y-%m-%d") if getattr(order, "order_date", None) else "",
        "receipt_address": getattr(order, "receipt_address", ""),
        "item": order.item,
        "quantity": order.quantity,
        "payway": getattr(order, "payway", ""),
        "note": order.note,
        "card_message": getattr(order, "card_message", ""),
        "weekday": getattr(order, "weekday", ""),
        "send_datetime": getattr(order, "send_datetime", ""),
        "receiver_name": getattr(order, "receiver_name", ""),
        "receiver_phone": getattr(order, "receiver_phone", ""),
        "delivery_address": getattr(order, "delivery_address", "")
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
