import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
from openai import OpenAI

# TODOS:
# 1. 建立資料庫，把上次該用戶是在什麼時候使用這個功能，以可以把過去的訂購資料過濾掉

load_dotenv()

# 讀取環境變數
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

app = Flask(__name__)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# GPT Prompt 模板
PROMPT_TEMPLATE = """
你是一個花店訂單生成助手，請從以下對話內容中，整理出以下資訊：
{   
    "customer_name": "", 
    "phone_number": "", 
    "flower_type": "", 
    "quantity": , 
    "budget": , 
    "pickup_method": "", 
    "pickup_date": "", 
    "pickup_time": "", 
    "Extra_requirements":"" 
}

請盡量確保內容正確性，如果你沒有辦法非常確定上面的資料，請填 NULL，或者是填寫原始對話在該欄位上。

對話內容：
{}

"""

@app.route("/callback", methods=['POST']) 
def callback():
    signature = request.headers['X-Line-Signature']
    if not signature:
        abort(400, description="Missing X-Line-Signature header")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature) # 用 handler.add() 來處理事件
    except InvalidSignatureError:
        abort(400, description="Invalid signature. Please check your channel access token and secret.")
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
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
