from core.database import SessionLocal
from models.order import Order
from models.user import User

def get_all_orders():
    session = SessionLocal()
    orders = session.query(Order).all()
    result = []

    for o in orders:
        user = session.query(User).filter_by(id=o.user_id).first()
        result.append({
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
    return result
