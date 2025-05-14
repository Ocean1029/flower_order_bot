import random
from datetime import datetime, timedelta
from app.models.order import Order, OrderDraft
from app.models.logistics import Shipment
from app.models.payment import Payment, PaymentMethod
from app.enums.payment import PaymentStatus
from faker import Faker

fake = Faker("zh_TW")

async def create_random_order(session, user, room):
    # 建立草稿訂單
    draft = OrderDraft(
        room_id=room.id,
        user_id=user.id,
        status="completed",
    )
    session.add(draft)
    await session.flush()  # 確保 draft.id 可用

    # 建立正式訂單
    total = round(random.uniform(1000, 3000), 2)
    order = Order(
        user_id=user.id,
        draft_id=draft.id,
        item_type=random.choice(["花束", "盆花"]),
        product_name=random.choice(["情人節限定", "母親節感恩", "開幕大吉"]),
        quantity=random.randint(1, 5),
        notes=fake.sentence(),
        card_message=fake.sentence(),
        receipt_address=fake.address(),
        total_amount=total,
        status="confirmed",
    )
    session.add(order)
    await session.flush()  # 確保 order.id 可用

    # 建立物流資訊
    shipment = Shipment(
        order_id=order.id,
        method=random.choice(["store_pickup", "delivery"]),
        status="pending",
        receiver_user_id=user.id,
        address=fake.address(),
        delivery_datetime=datetime.now() + timedelta(days=random.randint(1, 3)),
    )
    session.add(shipment)
    await session.flush()  # 確保 shipment.id 可用

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
