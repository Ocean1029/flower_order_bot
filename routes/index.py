from flask import Blueprint, render_template
from services.order_service import get_all_orders
from services.message_service import get_latest_messages
from services.stats_service import get_stats


index_bp = Blueprint("index", __name__)

@index_bp.route("/")
def dashboard():
    data = get_all_orders()
    messages = get_latest_messages()
    stats = get_stats()
    column_name = ["訂單ID", "姓名", "電話", "花材", "數量", "預算", "取貨方式", "取貨日期", "取貨時間", "備註"]

    return render_template("index.html", data=data, messages=messages, stats=stats, column_name=column_name)
