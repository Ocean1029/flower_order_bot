from flask import render_template
from flask import Response

from models import SessionLocal
from models.user import User
from models.order import Order



def setup_routes(app):
    @app.route("/orders")
    def orders():
        session = SessionLocal()
        orders = session.query(Order).all()
        data = []
        column_name = ["訂單ID", "姓名", "電話", "花材", "數量", "預算", "取貨方式", "取貨日期", "取貨時間", "備註"]

        for o in orders:
            user = session.query(User).filter_by(id=o.user_id).first()
            data.append({
                "id": o.id,
                "customer_name": user.customer_name if user else "未知",
                "phone": user.phone_number if user else "",
                "flower": o.flower_type,
                "qty": o.quantity,
                "budget": o.budget,
                "pickup_method": o.pickup_method,
                "pickup_date": o.pickup_date,
                "pickup_time": o.pickup_time,
                "note": o.extra_requirements
            })
        session.close()

        return render_template("orders.html", data=data, column_name=column_name)


    @app.route("/orders.csv")
    def export_orders_csv():
        session = SessionLocal()
        orders = session.query(Order).all()
        output = []

        output.append([
            "訂單ID", "姓名", "電話", "花材", "數量", "預算", "取貨方式", "取貨日期", "取貨時間", "備註"
        ])

        for o in orders:
            user = session.query(User).filter_by(id=o.user_id).first()
            output.append([
                o.id,
                user.customer_name if user else "未知",
                user.phone_number if user else "",
                o.flower_type,
                o.quantity,
                o.budget,
                o.pickup_method,
                o.pickup_date,
                o.pickup_time,
                o.extra_requirements,
            ])
        session.close()

        def generate():
            for row in output:
                yield ",".join([str(col) for col in row]) + "\n"

        return Response(
            generate(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=orders.csv"}
        )
