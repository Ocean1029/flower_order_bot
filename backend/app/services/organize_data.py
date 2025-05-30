from datetime import datetime, timedelta, timezone
from sqlalchemy import select, update
import json
from app.models.chat import ChatMessage, ChatRoom
from app.schemas.order import OrderDraftCreate, OrderDraftOut
from app.services.order_service import create_order_draft_by_room_id, get_order_draft_by_room, update_order_draft_by_room_id
from app.utils.line_send_message import LINE_push_message
from app.services.user_service import get_line_uid_by_chatroom_id
from fastapi import HTTPException, status
from app.managers.prompt_manager import PromptManager
from app.schemas.chat import ChatMessageBase
from openai import OpenAI
import os
from dotenv import load_dotenv
from decimal import Decimal
from app.enums.chat import ChatMessageStatus, ChatRoomStage, ChatMessageDirection


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)
prompt_manager = PromptManager()

def orm_to_dict(obj):
    if obj is None:
        return {}
    result = {}
    for c in obj.__table__.columns:
        value = getattr(obj, c.name)
        if isinstance(value, Decimal):
            value = float(value)
        elif isinstance(value, datetime):
            value = value.isoformat()
        result[c.name] = value
    return result

def _clean_parsed_reply(parsed_reply):
    for key, value in parsed_reply.items():
        if isinstance(value, str) and value.strip() == "":
            parsed_reply[key] = None
    return parsed_reply

async def organize_data(db, chat_room_id: int) -> OrderDraftOut:
    chat_room = await db.execute(
        select(ChatRoom).where(ChatRoom.id == chat_room_id)
    )
    chat_room = chat_room.scalars().first()
    if not chat_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到聊天室"
        )
    
    draft = await get_order_draft_by_room(db, chat_room.id)
    if not draft:
        print("🔍 找不到訂單草稿，正在建立新的草稿...")
        draft = create_order_draft_by_room_id(db, room_id=chat_room.id)
    
    
    stmt = select(ChatMessage).where(
        ChatMessage.room_id == chat_room_id,
        ChatMessage.processed == False
    ).order_by(ChatMessage.created_at.asc())

    result = await db.execute(stmt)
    messages = result.scalars().all()

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="過去 7 天內沒有尚未處理的對話資料喔～"
        )

    combined_text = "\n".join(
        reversed([f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {message.text} {message.direction}" for message in messages])
    )
    
    
    gpt_prompt = prompt_manager.load_prompt("order_prompt", user_message=combined_text, order_draft=json.dumps(orm_to_dict(draft)) or {})
    print("🔍 GPT 處理中...")
    print(f"📜 GPT Prompt:\n{gpt_prompt}")

    response = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "system", "content": gpt_prompt}],
        temperature=0
    )

    print("🔍 GPT 處理完成")
    print(f"💬 GPT 回覆:\n{response.choices[0].message.content.strip()}")

    gpt_reply = response.choices[0].message.content.strip()

    if not gpt_reply or gpt_reply.strip() == "":
        print("❗ GPT 回覆為空，無法解析")
        return None

    parsed_reply = _clean_parsed_reply(json.loads(gpt_reply))

    order_draft_create = OrderDraftCreate(
        customer_name=parsed_reply.get("customer_name"),
        customer_phone=parsed_reply.get("customer_phone"),
        receiver_name=parsed_reply.get("receiver_name"),
        receiver_phone=parsed_reply.get("receiver_phone"),
        pay_way=parsed_reply.get("pay_way"),
        total_amount=parsed_reply.get("total_amount"),
        item=parsed_reply.get("item"),
        quantity=parsed_reply.get("quantity"),
        note=parsed_reply.get("note"),
        card_message=parsed_reply.get("card_message"),
        shipment_method=parsed_reply.get("shipment_method"),
        send_datetime=parsed_reply.get("send_datetime"),
        receipt_address=parsed_reply.get("receipt_address"),
        delivery_address=parsed_reply.get("delivery_address"),
    )
    print(order_draft_create)

    # 傳送草稿中 缺漏的欄位傳給顧客
    missing_fields = []
    required_fields = {
        "customer_name": "顧客姓名",
        "customer_phone": "顧客電話",
        "receiver_name": "收件人姓名",
        "receiver_phone": "收件人電話",
        "pay_way": "付款方式",
        "total_amount": "總金額",
        "item": "商品項目",
        "quantity": "數量",
        "shipment_method": "配送方式",
        "send_datetime": "送達時間",
        "delivery_address": "收件地址"
    }
    for field, label in required_fields.items():
        if getattr(order_draft_create, field, None) in [None, "", 0]:
            missing_fields.append(label)

    if missing_fields:
        # 透過 chat_room_id 反查目前聊天室對應的 LINE UID
        line_uid = await get_line_uid_by_chatroom_id(db, chat_room.id)

        warning_msg = (
                "智慧客服已根據對話內容整理好訂單草稿囉！"
                "我們發現了一些缺少的資料，請幫我們直接在下方補上～\n"
                + "\n".join(f"- {f}" for f in missing_fields)
            )
        print(warning_msg)

        if line_uid:
            # 將字串包成 ChatMessageBase，再交給 LINE_push_message
            LINE_push_message(line_uid, ChatMessageBase(text=warning_msg))
            
            # 儲存提醒訊息的動作
            message = ChatMessage(
                room_id=chat_room.id,
                direction=ChatMessageDirection.OUTGOING_BY_BOT,
                text="[自動回覆已傳送]" + warning_msg,
                image_url="",
                status=ChatMessageStatus.PENDING,
                processed=True, # 之後不需要讓 GPT 讀到這個
                created_at=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None),
                updated_at=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)
                )
            db.add(message)
            await db.commit()
        else:
            print("❗ 無法取得該聊天室對應的 LINE UID，無法推播缺漏提醒。")

    # 更新訂單草稿
    order_draft_out = await update_order_draft_by_room_id(
        db=db,
        room_id=chat_room.id,
        draft_in=order_draft_create
    )
    print(f"訂單草稿已建立，ID：{order_draft_out.id}")
    
    # 將詳細資料印出來
    for key, value in order_draft_out.dict().items():
        if key not in ["id", "created_at", "updated_at"]:
            print(f"{key}: {value}")

    # 將對話訊息設為已處理
    stmt = update(ChatMessage)\
        .where(ChatMessage.id.in_([message.id for message in messages]))\
        .values(processed=True)
    await db.execute(stmt)
    await db.commit()

    return order_draft_out

