from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import PlainTextResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent
from openai import OpenAI
from sqlalchemy import select, update

from app.core.database import get_db
from app.models.chat import ChatRoom, ChatMessage
from app.models.user import User
from app.models.order import Order, OrderDraft
from app.managers.prompt_manager import PromptManager
from app.enums.chat import ChatRoomStage
from app.enums.order import OrderDraftStatus
from app.services.user_service import get_user_by_line_uid, create_user
from app.services.message_service import get_chat_room_by_user_id, create_chat_room

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
async def callback(request: Request, db: AsyncSession = Depends(get_db)):
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
async def handle_text_message(event: MessageEvent, db: AsyncSession):
    user_line_id = event.source.user_id # LINE ID
    user_message = event.message.text

    user = await get_user_by_line_uid(db, user_line_id)
    if not user:
        user = await create_user(db, user_line_id, "Profile Name")
        print(f"新使用者 {user_line_id} 已創建")
    else:
        print(f"使用者 {user_line_id} 已存在")
    
    # 取得或創建聊天室
    chat_room = await get_chat_room_by_user_id(db, user.id)
    if not chat_room:
        chat_room = await create_chat_room(db, user.id)
        print(f"新聊天室已創建，使用者 {user_line_id} 的聊天室 ID：{chat_room.id}")

    # 儲存訊息
    message = ChatMessage(
        room_id=chat_room.id,
        direction="incoming",
        text=user_message,
        image_url="",
        status="sent",
        processed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(message)
    await db.commit()
    await db.refresh(message)

    print(f"User {user_line_id} 發送訊息：{user_message}")


    if user_message == "整理資料":
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        stmt = select(ChatMessage).where(
            ChatMessage.room_id == chat_room.id,
            ChatMessage.created_at >= seven_days_ago,
            ChatMessage.processed == False
        ).order_by(ChatMessage.created_at.asc())

        result = await db.execute(stmt)
        messages = result.scalars().all()

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

        session_order_cache[user_line_id] = {
            "order_json": reply,
            "message_ids": [m.id for m in messages]
        }

        reply_text = f"以下是整理好的訂單資訊：\n{reply}\n\n如無誤請回覆：送出訂單。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

    elif user_message == "送出訂單" and user_line_id in session_order_cache:
        try:
            try:
                parsed = json.loads(session_order_cache[user_line_id]["order_json"])
            except json.JSONDecodeError as e:
                print("GPT 原始輸出：", session_order_cache[user_line_id]["order_json"])
                raise e

            message_ids = session_order_cache[user_line_id]["message_ids"]

            stmt = select(User).where(User.line_uid == user_line_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            

            order_draft = OrderDraft(
                user_id=user.id,
                room_id=chat_room.id,
                status=OrderDraftStatus.COLLECTING,
                item_type=parsed.get("item_type"),
                product_name=parsed.get("product_name"),
                quantity=parsed.get("quantity"),
                notes=parsed.get("notes"),
                card_message=parsed.get("card_message"),
                receipt_address=parsed.get("receipt_address"),
                total_amount=parsed.get("total_amount"),
                shipment_method=parsed.get("shipment_method"),
                shipment_status=parsed.get("shipment_status"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(order_draft)
            await db.commit()
            await db.refresh(order_draft)
            
            stmt = update(ChatMessage)\
                .where(ChatMessage.id.in_(message_ids))\
                .values(processed=True)
            await db.execute(stmt)
            await db.commit()
            del session_order_cache[user_line_id]

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="✅ 訂單已成功建立並儲存！感謝您！")
            )

        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"❌ 發生錯誤，請確認格式或稍後再試：{str(e)}")
            )
            

@handler.add(FollowEvent)
async def handle_follow(event: FollowEvent, db: AsyncSession):

    """
        1. get or create user
        2. get or create chat room
        3. send welcome template message
    """

    user_line_id = event.source.user_id
    user = await get_user_by_line_uid(db, user_line_id)
    if not user:
        user = await create_user(db, user_line_id, "Profile Name")
        print(f"新使用者 {user_line_id} 已創建")
    else:
        print(f"使用者 {user_line_id} 已存在")
    
    chat_room = await get_chat_room_by_user_id(db, user.id)
    if not chat_room:
        chat_room = await create_chat_room(db, user.id)
        print(f"新聊天室已創建，使用者 {user_line_id} 的聊天室 ID：{chat_room.id}")

    print("開始自動回覆流程")
    await run_bot_flow(chat_room, "", event, db)


# 控制 bot 自動回覆流程  By Benjamin
async def run_bot_flow(chat_room: ChatRoom, text: str, event: MessageEvent, db: AsyncSession):
    STEP_MAP = {
        0: ask_color,
        1: ask_budget,
        # 2: ask_special,
        # 3: final_confirm,
    }

    # ── 1. 根據 bot_step 叫對的 handler
    handler = STEP_MAP.get(chat_room.bot_step)  # Handler 一定會回傳 (nextstep, manual_override)

    if handler is None: # 如果找不到對應的 handler，表示 bot_step 錯誤
        print(f"Error: No handler for bot_step {chat_room.bot_step}, reset bot_step to 0")
        chat_room.bot_step = 0
        chat_room.stage = ChatRoomStage.MANUAL
        await db.commit()
        return

    # ── 2. 執行該節點邏輯，並取得下一步
    next_step, manual_override = await handler(text, event, db)

    if manual_override:
        chat_room.stage = ChatRoomStage.WAITING_OWNER
        chat_room.bot_step = -1
    else:
        chat_room.bot_step = next_step
        if next_step == -1:
            chat_room.stage = ChatRoomStage.WAITING_OWNER

    await db.commit()

async def ask_color(user_text, event, db):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("想要什麼顏色的客製化花束？")
    )
    return 0, False   # stay on step 0 等用戶回答

    # 第二回合：收集使用者顏色
    color = user_text.strip()
    # TODO validate color, save into draft table
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("好的～預算大概多少呢？")
    )
    return 1, False   # 下一節點 = 1（ask_budget）

# ── 2. 預算詢問
async def ask_budget(user_text, event, db):
    budget = user_text.strip() 
    # TODO validate, save
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("👌 了解！已記錄～我們客服會盡快聯繫你確認細節。")
    )
    return -1, False  # -1 = flow finished

# ── 3. 特別需求詢問 之類的


# Handler 到這裡結束