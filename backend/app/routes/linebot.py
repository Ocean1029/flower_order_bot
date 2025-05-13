from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi.responses import PlainTextResponse
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from openai import OpenAI

from app.core.database import get_db
from app.models.chat import ChatMessage
from app.models.user import User
from app.models.order import Order
from app.managers.prompt_manager import PromptManager

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# 加在全域暫存區（部署時可用 Redis or DB 儲存）
session_order_cache = {}  # key: user_id, value: GPT 整理的 JSON

# 讀取環境變數
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

prompt_manager = PromptManager()

api_router = APIRouter()

@api_router.post("/callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        raise HTTPException(status_code=400, detail="Missing X-Line-Signature header")

    body = await request.body()
    body_str = body.decode('utf-8')

    try:
        events = handler.parser.parse(body_str, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            await handle_text_message(event, db)

    return PlainTextResponse('OK')

@handler.add(MessageEvent, message=TextMessage)
async def handle_text_message(event: MessageEvent, db: Session):
    user_id = event.source.user_id
    user_message = event.message.text

    # 儲存訊息
    msg = ChatMessage(
        room_id=None,
        direction="incoming",
        text=user_message,
        status="sent"
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    if user_message == "整理資料":
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        messages = db.query(ChatMessage)\
            .filter(
                ChatMessage.room_id == None,
                ChatMessage.created_at >= seven_days_ago,
                ChatMessage.processed == False
            )\
            .order_by(ChatMessage.created_at.asc())\
            .all()

        if not messages:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="過去 7 天內沒有尚未處理的對話資料喔～")
            )
            return

        combined_text = "\n".join(reversed([m.text for m in messages]))
        gpt_prompt = prompt_manager.load_prompt("order_prompt", user_message=combined_text)

        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "system", "content": gpt_prompt}],
            temperature=0
        )
        reply = response.choices[0].message.content.strip()

        session_order_cache[user_id] = {
            "order_json": reply,
            "message_ids": [m.id for m in messages]
        }

        reply_text = f"以下是整理好的訂單資訊：\n{reply}\n\n如無誤請回覆：送出訂單。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

    elif user_message == "送出訂單" and user_id in session_order_cache:
        try:
            try:
                parsed = json.loads(session_order_cache[user_id]["order_json"])
            except json.JSONDecodeError as e:
                print("GPT 原始輸出：", session_order_cache[user_id]["order_json"])
                raise e

            message_ids = session_order_cache[user_id]["message_ids"]

            user = db.query(User).filter_by(line_uid=user_id).first()
            if not user:
                user = User(
                    line_uid=user_id,
                    name=parsed.get("customer_name"),
                    phone=parsed.get("phone_number")
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            order = Order(
                user_id=user.id,
                item_type=parsed.get("item_type"),
                product_name=parsed.get("product_name"),
                quantity=parsed.get("quantity"),
                notes=parsed.get("notes"),
                card_message=parsed.get("card_message"),
                receipt_address=parsed.get("receipt_address"),
                total_amount=parsed.get("total_amount", 0)
            )
            db.add(order)

            db.query(ChatMessage).filter(ChatMessage.id.in_(message_ids))\
              .update({"processed": True}, synchronize_session=False)

            db.commit()
            del session_order_cache[user_id]

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="✅ 訂單已成功建立並儲存！感謝您！")
            )

        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"❌ 發生錯誤，請確認格式或稍後再試：{str(e)}")
            )