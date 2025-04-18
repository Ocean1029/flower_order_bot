from flask import render_template
from flask import Response

from models import SessionLocal
from models.user import User
from models.order import Order
from models.message import Message
from sqlalchemy import func, desc
from datetime import datetime


def setup_routes(app):
    @app.route("/")
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

        subquery = session.query(
            Message.user_id,
            func.max(Message.timestamp).label("latest_time")
        ).group_by(Message.user_id).subquery()

        latest_messages = session.query(Message).join(
            subquery,
            (Message.user_id == subquery.c.user_id) &
            (Message.timestamp == subquery.c.latest_time)
        ).order_by(desc(Message.timestamp)).all()

        # 🔹 組裝給前端的 message 資料
        messages = []
        for msg in latest_messages:
            user = session.query(User).filter_by(line_id=msg.user_id).first()
            messages.append({
                "id": msg.id,
                "customer_name": user.customer_name if user else "",
                "phone": user.phone_number if user else "",
                "preview": msg.text[:40],  # 最多 40 字
                "time": msg.timestamp.strftime("%Y-%m-%d %H:%M")
            })

        # 🔹 今日起始時間
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        month_start = datetime(now.year, now.month, 1)

        # 🔹 計算統計值
        today_orders = session.query(Order).filter(Order.created_at >= today_start).count()
        total_customers = session.query(User).count()
        monthly_income = session.query(func.coalesce(func.sum(Order.budget), 0)).filter(Order.created_at >= month_start).scalar()
        pending_orders = session.query(Order).count()  # 未來要 filter by status

        stats = {
            "today_orders": today_orders,
            "pending_orders": pending_orders,
            "monthly_income": monthly_income,
            "total_customers": total_customers
        }

        return render_template("index.html", data=data, stats=stats, messages=messages, column_name=column_name)


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
