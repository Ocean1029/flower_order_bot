from datetime import datetime, timedelta
from sqlalchemy import select, update
import json
from app.models.chat import ChatMessage, ChatRoom
from app.schemas.order import OrderDraftCreate, OrderDraftOut
from app.services.order_service import create_order_draft_by_room_id, get_order_draft
from fastapi import HTTPException, status
from app.managers.prompt_manager import PromptManager
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)
prompt_manager = PromptManager()

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
    
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    stmt = select(ChatMessage).where(
        ChatMessage.room_id == chat_room_id,
        ChatMessage.created_at >= seven_days_ago,
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
        reversed([f"[{m.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {m.text}" for m in messages])
    )

    # from sqlalchemy.orm import class_mapper

    # def orm_to_dict(obj):
    #     result = {}
    #     for c in class_mapper(obj.__class__).columns:
    #         val = getattr(obj, c.key)
    #         if isinstance(val, datetime):
    #             result[c.key] = val.isoformat()
    #         else:
    #             result[c.key] = val
    #     return result
    
    draft = await get_order_draft(db, chat_room.id)
    
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
        customer_name=parsed_reply.get("name"),
        customer_phone=parsed_reply.get("phone"),
        receiver_name=parsed_reply.get("receiver_name"),
        receiver_phone=parsed_reply.get("receiver_phone"),
        pay_way_id=parsed_reply.get("pay_way_id"),
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
    order_draft_out = await create_order_draft_by_room_id(db=db, room_id=chat_room.id, draft_in=order_draft_create)
    print(f"訂單草稿已建立，ID：{order_draft_out.id}")
    
    # # 將詳細資料印出來
    # for key, value in order_draft_out.dict().items():
    #     if key not in ["id", "created_at", "updated_at"]:
    #         print(f"{key}: {value}")

    # 將對話訊息設為已處理
    stmt = update(ChatMessage)\
        .where(ChatMessage.id.in_([message.id for message in messages]))\
        .values(processed=True)
    await db.execute(stmt)
    await db.commit()

    return order_draft_out
