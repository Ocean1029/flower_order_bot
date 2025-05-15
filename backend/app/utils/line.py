# backend/app/services/chat.py

import os

from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
import logging
from linebot.models import TextSendMessage, ImageSendMessage
from app.enums.chat import ChatMessageDirection
from app.schemas.chat import (
    ChatMessageBase,
)

# ──────────────────────────────
#  LINE PUSH 基本設定
# ──────────────────────────────
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


def LINE_push_message(line_uid: str, data: ChatMessageBase) -> bool: 
    """
    發送訊息到 LINE
    :param line_uid: 使用者的 LINE UID
    :param data: 訊息內容
    """
    try:
        if data.text:
            line_bot_api.push_message(
                line_uid, 
                TextSendMessage(text=data.text)
            )
        elif data.image_url:
            line_bot_api.push_message(
                line_uid,
                ImageSendMessage(
                    original_content_url=data.image_url,
                    preview_image_url=data.image_url,
                ),
            )
        return True

    except LineBotApiError as e:
        logging.error(f"[LINE PUSH] 送出失敗：{e.status_code} - {e.error.message}")
        return False

    except Exception as e:
        logging.exception(f"[LINE PUSH] 未知錯誤：{str(e)}")
        return False