from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import PlainTextResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent
from linebot.models import QuickReply, QuickReplyButton, MessageAction
from openai import OpenAI
from sqlalchemy import select, update

from app.core.database import get_db
from app.models.chat import ChatRoom, ChatMessage
from app.models.user import User
from app.models.order import Order, OrderDraft
from app.managers.prompt_manager import PromptManager
from app.enums.chat import ChatRoomStage
from app.enums.order import OrderDraftStatus
from app.services.user_service import get_user_by_line_uid, create_user, update_user_info
from app.services.message_service import get_chat_room_by_user_id, create_chat_room
from app.utils.line_send_message import send_quick_reply_message, send_confirm
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
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

    if user_message == "Again":
        # 回到 welcome, -1
        chat_room.stage = ChatRoomStage.WELCOME
        chat_room.bot_step = -1
        await db.commit()
        db.refresh(chat_room)
        print("回到 welcome")
        return

    if chat_room.stage == ChatRoomStage.WELCOME:
        await run_welcome_flow(chat_room, user_message, event, db)
        return

    # Bot 自動回覆流程
    if chat_room.stage == ChatRoomStage.BOT_ACTIVE:
        await run_bot_flow(chat_room, user_message, event, db)
        return



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
        gpt_reply = response.choices[0].message.content.strip()
        parsed_reply = json.loads(gpt_reply)

        reply_text = f"以下是整理好的訂單資訊：\n{gpt_reply}\n\n，請確認資訊。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )


        user = await update_user_info(
            db,
            user.id,
            name=parsed_reply.get("name"),
            phone=parsed_reply.get("phone"),
        )

        order_draft = OrderDraft(
            user_id=user.id,
            room_id=chat_room.id,
            status=OrderDraftStatus.COLLECTING,
            item_type=parsed_reply.get("item_type"),
            product_name=parsed_reply.get("product_name"),
            quantity=parsed_reply.get("quantity"),
            notes=parsed_reply.get("notes", ""),
            card_message=parsed_reply.get("card_message", ""),
            receipt_address=parsed_reply.get("receipt_address", ""),
            total_amount=parsed_reply.get("total_amount"),
            shipment_method=parsed_reply.get("shipment_method"),
            shipment_status=parsed_reply.get("shipment_status"),
            # delivery_datetime=parsed_reply.get("delivery_datetime"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(order_draft)
        await db.commit()
        await db.refresh(order_draft)
    
        stmt = update(ChatMessage)\
            .where(ChatMessage.id.in_([message.id for message in messages]))\
            .values(processed=True)
        await db.execute(stmt)
        await db.commit()

        


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



# Welcome 流程 By Benjamin

# ──────────────────────────────────────────────────────────────
# Welcome flow：先確認是否要走客製化花束流程
async def run_welcome_flow(
    chat_room: ChatRoom,
    user_text: str,
    event: MessageEvent,
    db: AsyncSession,
):
    """
    1) 第一次進入時 (bot_step == -1) -> 發出詢問
    2) 第二次收到使用者回覆 -> 根據答案切換 stage
       - yes / 是  -> BOT_ACTIVE
       - 其他      -> WAITING_OWNER
    """
    if chat_room.bot_step == -1:  # 第一次進入
        send_confirm(
            event.reply_token,
            "想要客製化花束嗎？",
            yes_txt="是",
            no_txt="否",
            yes_reply="啟動智慧訂購流程",
            no_reply="直接轉接老闆"
        )
        chat_room.bot_step = 0  # 記錄 bot_step 為 0，表示已詢問過
        await db.commit()
        db.refresh(chat_room)
        print("已詢問使用者是否要客製化花束")
        return
    
    # 第二次收到使用者回覆
    if user_text == "啟動智慧訂購流程":
        chat_room.stage = ChatRoomStage.BOT_ACTIVE
        chat_room.bot_step = 0  # reset for bot flow start
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("了解！我們開始客製化流程～")
        )
    else:
        chat_room.stage = ChatRoomStage.WAITING_OWNER
        chat_room.bot_step = -1
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("好的！已轉交給客服人員，請稍候。")
        )

    await db.commit()


# 控制 bot 自動回覆流程  By Benjamin
async def run_bot_flow(chat_room: ChatRoom, text: str, event: MessageEvent, db: AsyncSession):
    STEP_MAP = {
        0: ask_color,
        2: ask_budget,
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
        if next_step == -1:  # flow finished
            chat_room.stage = ChatRoomStage.WAITING_OWNER

    await db.commit()

async def ask_color(user_text, event, db):
    """
    Step 0: ask color by quick‑reply buttons.
    This function is called twice:
    1) When bot_step == 0 and bot still waits for user -> just ask the question.
    2) After user clicks a quick‑reply button -> capture answer and move on.
    """
    if user_text == "":  # first entry triggered by FollowEvent
        send_quick_reply_message(
            event.reply_token,
            "想要什麼顏色的客製化花束？",
            ["紅", "白", "粉", "其他"]
        )
        return 0, False  # stay on the same step waiting for input
    # second round: user answered → proceed
    # TODO: persist `color` into draft table
    send_quick_reply_message(
        event.reply_token,
        "好的～預算大概多少呢？",
        ["500以下", "500-1000", "1000以上"]
    )
    return 2, False

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

