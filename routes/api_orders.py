from flask import Blueprint, Response, jsonify
from services.order_service import get_all_orders

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders.csv")
def export_orders_csv():
    data = get_all_orders()

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

    def generate():
        for row in output:
            yield ",".join([str(col) for col in row]) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=orders.csv"}
    )

def get_orders():
    orders = get_all_orders()
    return jsonify({"orders": orders})

api_orders_bp = Blueprint('api_orders', __name__)

@api_orders_bp.route("/api/orders", methods=["GET"])
def get_orders():
    orders = get_all_orders()
    return jsonify({"orders": orders})
