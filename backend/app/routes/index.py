from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.services.order_service import get_all_orders
from app.services.message_service import get_latest_messages
from app.services.stats_service import get_stats

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    data = get_all_orders()
    messages = get_latest_messages()
    stats = get_stats()
    column_name = ["訂單ID", "姓名", "電話", "花材", "數量", "預算", "取貨方式", "取貨日期", "取貨時間", "備註"]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": data,
            "messages": messages,
            "stats": stats,
            "column_name": column_name
        }
    )
