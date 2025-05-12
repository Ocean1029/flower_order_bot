from app.core.database import SessionLocal
from models.order import Order
from models.user import User 
from sqlalchemy import func
from datetime import datetime

def get_stats():
    session = SessionLocal()
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    month_start = datetime(now.year, now.month, 1)

    today_orders = session.query(Order).filter(Order.created_at >= today_start).count()
    total_customers = session.query(User).count()
    monthly_income = session.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(Order.created_at >= month_start).scalar()
    pending_orders = session.query(Order).count()

    session.close()
    return {
        "today_orders": today_orders,
        "pending_orders": pending_orders,
        "monthly_income": monthly_income,
        "total_customers": total_customers
    }
