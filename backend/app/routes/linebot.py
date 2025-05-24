from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import PlainTextResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
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
from app.enums.order import OrderDraftStatus, OrderStatus
from app.enums.chat import ChatMessageStatus, ChatRoomStage, ChatMessageDirection
from app.schemas.user import UserCreate
from app.schemas.order import OrderDraftCreate
from app.services.user_service import get_user_by_line_uid, create_user, update_user_info
from app.services.message_service import get_chat_room_by_user_id, create_chat_room
from app.services.order_service import create_order_draft_by_room_id
from app.utils.line_send_message import send_quick_reply_message, send_confirm
from app.utils.line_get_profile import fetch_user_profile
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
    user_line_id = event.source.user_id 
    user_message = event.message.text

    user = await get_user_by_line_uid(db, user_line_id)
    if not user:
        # 取得使用者資料
        profile = await fetch_user_profile(user_line_id)
        if profile:
            user_name = profile.display_name
            user_status = profile.status_message
            print(f"使用者名稱: {user_name}, 使用者狀態: {user_status}")
        else:
            user_name = "Unknown"
            print("無法獲取使用者資料")
        user = await create_user(db, UserCreate(
            line_uid=user_line_id,
            name=user_name,
            phone="",
        ))
    
    # 取得或創建聊天室
    chat_room = await get_chat_room_by_user_id(db, user.id)
    if not chat_room:
        chat_room = await create_chat_room(db, user.id)
        print(f"新聊天室已創建，使用者 {user_line_id} 的聊天室 ID：{chat_room.id}")

    # 儲存訊息
    message = ChatMessage(
        room_id=chat_room.id,
        direction=ChatMessageDirection.INCOMING,
        text=user_message,
        image_url="",
        status=ChatMessageStatus.PENDING,
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
        await db.refresh(chat_room)
        print("回到 welcome")
        return

    if chat_room.stage == ChatRoomStage.WELCOME:
        await run_welcome_flow(chat_room, user_message, event, db)
        await db.refresh(chat_room)  # 如果變成BOT_Active 要直接進入bot流程
        if chat_room.stage == ChatRoomStage.BOT_ACTIVE:
            await run_bot_flow(chat_room, "", event, db)
        return

    # if chat_room.stage == ChatRoomStage.ORDER_CONFIRM:
    #     await run_order_confirm_flow(
    #         chat_room, user_message, user_line_id, event, db
    #     )
    #     return

    # Bot 自動回覆流程
    if chat_room.stage == ChatRoomStage.BOT_ACTIVE:
        await run_bot_flow(chat_room, user_message, event, db)
        return


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
        await db.refresh(chat_room)
        print("已詢問使用者是否要客製化花束")
        return
    
    # 第二次收到使用者回覆
    if user_text == "啟動智慧訂購流程":
        chat_room.stage = ChatRoomStage.BOT_ACTIVE
        chat_room.bot_step = 1  # reset for bot flow start
        
        # 不能回東西，reply_message 只能一次
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage("了解！我們開始客製化流程～")
        # )
    else:
        chat_room.stage = ChatRoomStage.WAITING_OWNER
        chat_room.bot_step = -1
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("好的！已轉交給客服人員，請稍候。")
        )

    await db.commit()
    db.refresh(chat_room)


# ──────────────────────────────────────────────────────────────

async def run_bot_flow(chat_room: ChatRoom, text: str, event: MessageEvent, db: AsyncSession):
    STEP_MAP = {
        1: ask_budget,
        2: ask_color,
        3: ask_type,
        4: last,
    }

    while True:
        handler = STEP_MAP.get(chat_room.bot_step)

        if handler is None:
            print(f"Error: No handler for bot_step {chat_room.bot_step}, reset bot_step to 0")
            chat_room.bot_step = 0
            chat_room.stage = ChatRoomStage.WAITING_OWNER
            await db.commit()
            return

        # ── 2. 執行該節點邏輯，並取得下一步
        next_step, manual_override, next_question = await handler(text, event, db, chat_room)

        if manual_override:
            chat_room.stage = ChatRoomStage.WAITING_OWNER
            chat_room.bot_step = -1
        else:
            chat_room.bot_step = next_step
            if next_step == -1:  # flow finished
                chat_room.stage = ChatRoomStage.WAITING_OWNER

        await db.commit()
        
        if not next_question: 
            break


async def ask_budget(user_text, event, db, chat_room):
    if chat_room.bot_step == 1:
        if user_text.strip() == "":
            send_quick_reply_message(
                event.reply_token,
                "好的～預算大概多少呢？",
                ["500以下", "500-1000", "1000以上"]
            )
            return 1, False, False
        else:
            budget = user_text.strip()
            # 根據預算決定下一步流程
            if budget == "500以下":
                return 2, False, True
            else:
                # 中高價位 → 問顏色
                return 3, False, True
    
async def ask_color(user_text, event, db, chat_room):

    if chat_room.bot_step == 2:
        send_quick_reply_message(
            event.reply_token,
            "想要什麼顏色的客製化花束？",
            ["紅", "白", "粉", "其他"]
        )
        return 4, False, False  # stay on the same step waiting for input
    
async def ask_type(user_text, event, db, chat_room):
    if chat_room.bot_step == 3:
        send_quick_reply_message(
            event.reply_token,
            "想要什麼類型的花材？",
            ["大欸米", "中欸米", "小欸米", "其他"]
        )
        return 4, False, False  # stay on the same step waiting for input

async def last(user_text, event, db, chat_room):
    
    budget = user_text.strip()
    # TODO validate, save
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("👌 了解！已記錄～我們客服會盡快聯繫你確認細節。")
    )
    return -1, False, False  # flow finished

# ── 3. 特別需求詢問 之類的

# Handler 到這裡結束

