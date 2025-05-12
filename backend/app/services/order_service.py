from app.core.database import SessionLocal
from models.order import Order
from models.user import User
from models.logistics import Shipment

def get_all_orders():
    session = SessionLocal()
    orders = session.query(Order).all()
    result = []

    for o in orders:
        user = session.query(User).filter_by(id=o.user_id).first()
        shipment = session.query(Shipment).filter_by(order_id=o.id).first()

        result.append({
            "id": o.id,
            "customer_name": user.name if user else "未知",
            "phone": user.phone if user else "",
            "item_type": o.item_type,
            "product_name": o.product_name,
            "quantity": o.quantity,
            "total_amount": float(o.total_amount) if o.total_amount else None,
            "note": o.notes or "",
            "pickup_method": shipment.method if shipment else "未知",
            "pickup_datetime": shipment.delivery_datetime.strftime("%Y-%m-%d %H:%M") if shipment and shipment.delivery_datetime else "",
        })
    session.close()
    return result
