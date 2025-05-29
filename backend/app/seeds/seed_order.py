import random
from datetime import datetime, timedelta, timezone
from app.models.order import Order, OrderDraft
from app.models.payment import Payment, PaymentMethod
from app.models.user import User
from app.enums.payment import PaymentStatus
from app.enums.order import OrderStatus
from app.enums.shipment import ShipmentMethod, ShipmentStatus
from faker import Faker
from sqlalchemy import select
from app.models.chat import ChatRoom

fake = Faker("zh_TW")

async def create_id_prefix(session, serial_number) -> str:
    """Create a prefix based on the current date in yymmddMMM format."""
    id_prefix = datetime.now(timezone(timedelta(hours=8))).strftime("%y%m%d")
    id = f"{id_prefix}{serial_number:03d}"
    return id

async def create_random_order(session, user: User, serial_number: int) -> Order:
    # 建立草稿訂單
    total = round(random.uniform(1000, 3000), 0) 
    quantity = random.randint(1, 5)
    note = fake.sentence(nb_words=10)
    card = fake.sentence(nb_words=5)
    delivery_datetime = datetime.now(timezone(timedelta(hours=8))) + timedelta(days=random.randint(1, 3))
    shipment_method = random.choice([ShipmentMethod.STORE_PICKUP, ShipmentMethod.DELIVERY])
    item_type = random.choice(["花束", "盆花"])
    
    # 獲取使用者的聊天室
    chat_room = await session.execute(
        select(ChatRoom).where(ChatRoom.user_id == user.id)
    )
    chat_room = chat_room.scalar_one()
    
    # 建立正式訂單
    order = Order(
        id=await create_id_prefix(session, serial_number),
        room_id=chat_room.id,  # 使用使用者的聊天室ID
        user_id=user.id,
        receiver_user_id=user.id,  # 預設收件人就是訂購人

        status=OrderStatus.CONFIRMED,

        item_type=item_type,
        quantity=quantity,
        notes=note,
        card_message=card,
        receipt_address=fake.address() if shipment_method == ShipmentMethod.DELIVERY else None,
        total_amount=total,
        shipment_method=shipment_method,
        shipment_status=ShipmentStatus.PENDING,
        delivery_address=fake.address() if shipment_method == ShipmentMethod.DELIVERY else None,
        delivery_datetime=delivery_datetime,
    )
    session.add(order)
    await session.flush()  # 確保 order.id 可用

    # # 取得一個啟用的付款方式
    # payment_method = (
    #     await session.execute(
    #         PaymentMethod.__table__.select().where(PaymentMethod.active.is_(True))
    #     )
    # ).first()

    # if payment_method is None:
    #     payment_method = PaymentMethod(display_name="信用卡", code="credit_card", instructions="請至官網付款")
    #     session.add(payment_method)
    #     await session.flush()
        
    # # 建立付款紀錄
    # payment = Payment(
    #     order_id=order.id,
    #     method_id=payment_method.id,
    #     amount=total,
    #     status=PaymentStatus.PAID,
    #     paid_at=datetime.now(timezone(timedelta(hours=8))),
    #     confirmed_at=datetime.now(timezone(timedelta(hours=8))),
    # )
    # session.add(payment)

    return order
