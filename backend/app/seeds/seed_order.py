import random
from datetime import datetime, timedelta
from app.models.order import Order, OrderDraft
from app.models.payment import Payment, PaymentMethod
from app.enums.payment import PaymentStatus
from app.enums.order import OrderStatus, OrderDraftStatus
from app.enums.shipment import ShipmentMethod, ShipmentStatus
from faker import Faker
from sqlalchemy import select
from app.models.chat import ChatRoom

fake = Faker("zh_TW")

async def create_random_order(session, user):
    # 建立草稿訂單
    total = round(random.uniform(1000, 3000), 2)
    delivery_datetime = datetime.now() + timedelta(days=random.randint(1, 3))
    shipment_method = random.choice([ShipmentMethod.STORE_PICKUP, ShipmentMethod.DELIVERY])
    item_type = random.choice(["花束", "盆花"])
    
    # 隨機選擇一個聊天室
    room = await session.execute(
        select(ChatRoom).where(ChatRoom.user_id == user.id)
    )
    room = room.scalars().first()
    
    if room is None:
        raise ValueError("找不到聊天室")

    draft = OrderDraft(
        room_id=room.id,
        user_id=user.id,
        receiver_user_id=user.id,  # 預設收件人就是訂購人
        status=OrderDraftStatus.COMPLETED,
        item_type=item_type,
        quantity=random.randint(1, 5),
        total_amount=total,
        notes=fake.sentence(),
        card_message=fake.sentence(),
        shipment_method=shipment_method,
        shipment_status=ShipmentStatus.PENDING,
        receipt_address=fake.address(),
        delivery_address=fake.address() if shipment_method == ShipmentMethod.DELIVERY else None,
        delivery_datetime=delivery_datetime if shipment_method == ShipmentMethod.DELIVERY else None,
    )
    session.add(draft)
    await session.flush()  # 確保 draft.id 可用

    # 建立正式訂單
    order = Order(
        user_id=user.id,
        receiver_user_id=user.id,  # 預設收件人就是訂購人
        draft_id=draft.id,
        item_type=item_type,
        quantity=draft.quantity,
        notes=draft.notes,
        card_message=draft.card_message,
        receipt_address=draft.receipt_address,
        total_amount=total,
        status=OrderStatus.CONFIRMED,
        shipment_method=shipment_method,
        shipment_status=ShipmentStatus.PENDING,
        delivery_address=draft.delivery_address,
        delivery_datetime=draft.delivery_datetime,
    )
    session.add(order)
    await session.flush()  # 確保 order.id 可用

    # 取得一個啟用的付款方式
    payment_method = (
        await session.execute(
            PaymentMethod.__table__.select().where(PaymentMethod.active.is_(True))
        )
    ).first()

    if payment_method is None:
        payment_method = PaymentMethod(display_name="信用卡", code="credit_card", instructions="請至官網付款")
        session.add(payment_method)
        await session.flush()
        
    # 建立付款紀錄
    payment = Payment(
        order_id=order.id,
        method_id=payment_method.id,
        amount=total,
        status=PaymentStatus.PAID,
        paid_at=datetime.now(),
        confirmed_at=datetime.now(),
    )
    session.add(payment)

    return order
