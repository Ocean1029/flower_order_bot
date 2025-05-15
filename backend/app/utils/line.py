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
from linebot.models import QuickReply, QuickReplyButton, MessageAction

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
    

# ──────────────────────────────────────────────────────────────
def send_quick_reply_message(reply_token: str, text: str, options: list[str]):
    """
    Helper to send a text message with LINE quick‑reply buttons.
    `options` is a list of button labels / text payload (kept identical).
    """
    items = [
        QuickReplyButton(action=MessageAction(label=opt, text=opt))
        for opt in options
    ]
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text=text, quick_reply=QuickReply(items=items))
    )
# ──────────────────────────────────────────────────────────────

from linebot.models import ConfirmTemplate, TemplateSendMessage, MessageAction

def send_confirm(reply_token: str, text: str,
                 yes_txt="是", no_txt="否", yes_reply="yes", no_reply="no"):
    tpl = ConfirmTemplate(
        text=text,
        actions=[
            MessageAction(label=yes_txt, text=yes_reply),
            MessageAction(label=no_txt, text=no_reply)
        ]
    )
    line_bot_api.reply_message(
        reply_token,
        TemplateSendMessage(alt_text=text, template=tpl)
    )

