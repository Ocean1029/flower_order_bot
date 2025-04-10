import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 讀取環境變數
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

openai_client = OpenAI(api_key=OPENAI_API_KEY)

# GPT Prompt 模板
PROMPT_TEMPLATE = """
你是一個花店訂單生成助手，從以下對話中，整理出顧客姓名、聯絡電話、花材種類、顏色、數量大小、取貨時間、特殊需求（如果沒有填空即可）：

對話內容：
{}

回傳 JSON 格式。
"""

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT_TEMPLATE.format(user_message)},
        ],
        temperature=0
    )

    order_info = response.choices[0].message.content.strip()
    # order_info = "test"

    # 回覆訂單資訊給使用者
    reply_text = f"以下是您的訂單資訊：\n{order_info}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(port=8000, debug=True)
