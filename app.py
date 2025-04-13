import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
from openai import OpenAI
from models import Message, SessionLocal
from datetime import datetime, timedelta

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
{{   
    "customer_name": "", 
    "phone_number": "", 
    "flower_type": "", 
    "quantity": , 
    "budget": , 
    "pickup_method": "", 
    "pickup_date": "", 
    "pickup_time": "", 
    "Extra_requirements":"" 
}}

請盡量確保內容正確性，如果你沒有辦法非常確定上面的資料，請填 NULL，或者是填寫原始對話在該欄位上。

對話內容：
{user_message}

回傳的格式為 JSON 格式，並且請確保 JSON 格式正確，並且沒有多餘的空格或換行。
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

    session = SessionLocal()
    user_id = event.source.user_id
    user_message = event.message.text

    # 儲存訊息
    msg = Message(user_id=user_id, text=user_message)
    session.add(msg)
    session.commit()

    if user_message == "整理資料":
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        messages = session.query(Message)\
            .filter(
                Message.user_id == user_id,
                Message.timestamp >= seven_days_ago
            )\
            .order_by(Message.timestamp.asc())\
            .all()
        
        # 轉成一段文字對話紀錄
        combined_text = "\n".join(reversed([m.text for m in messages]))

        gpt_prompt = PROMPT_TEMPLATE.format(user_message=combined_text)

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": gpt_prompt},
            ],
            temperature=0
        )
        
        reply = response.choices[0].message.content.strip()
        reply_text = f"以下是整理好的訂單資訊：\n{reply}"
        # 回覆用戶
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

    session.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) # render deployment default port
    app.run(host="0.0.0.0", port=port, debug=True)
