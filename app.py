import os
from dotenv import load_dotenv
import json
import csv
from datetime import datetime, timedelta

from flask import Flask, request, abort
from flask import render_template
from flask import Response

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from openai import OpenAI

from models import SessionLocal
from models.user import User
from models.order import Order
from models.message import Message


load_dotenv()

# 加在全域暫存區（部署時可用 Redis or DB 儲存）
session_order_cache = {}  # key: user_id, value: GPT 整理的 JSON

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
你是一個花店訂單生成助手，請從以下對話內容中，並用合法 JSON 格式回傳。注意：

- 每個欄位都必須填入值，若沒有請填 `null`
- 不要有任何註解、多餘文字、換行

格式如下：

{{
    "customer_name": "",
    "phone_number": "",
    "flower_type": "",
    "quantity": null,
    "budget": null,
    "pickup_method": "",
    "pickup_date": "",
    "pickup_time": "",
    "Extra_requirements": ""
}}

請盡量確保內容正確性，如果你沒有辦法非常確定上面的資料，請填 null。

對話內容：
{user_message}
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
                Message.timestamp >= seven_days_ago,
                Message.used == False
            )\
            .order_by(Message.timestamp.asc())\
            .all()
        
        # 如果沒有找到符合條件的訊息，則回覆用戶，但理論上不會發生。
        if not messages:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="過去 7 天內沒有尚未處理的對話資料喔～")
            )
            session.close()
            return
        

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
        
        # 暫存 GPT 整理結果
        session_order_cache[user_id] = {
            "order_json": reply,
            "message_ids": [m.id for m in messages]
        }

        reply_text = f"以下是整理好的訂單資訊：\n{reply}\n\n如無誤請回覆：資料正確。"
        # 回覆用戶
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    
    elif user_message == "資料正確" and user_id in session_order_cache:
        try:
            try:
                parsed = json.loads(session_order_cache[user_id]["order_json"])
            except json.JSONDecodeError as e:
                print("GPT 原始輸出：", session_order_cache[user_id]["order_json"])
                raise e
            message_ids = session_order_cache[user_id]["message_ids"]

            # 查或建使用者
            user = session.query(User).filter_by(line_id=user_id).first()
            if not user:
                user = User(
                    line_id=user_id,
                    customer_name=parsed.get("customer_name"),
                    phone_number=parsed.get("phone_number")
                )
                session.add(user)
                session.commit()

            # 建立訂單
            order = Order(
                user_id=user.id,
                flower_type=parsed.get("flower_type"),
                quantity=parsed.get("quantity"),
                budget=parsed.get("budget"),
                pickup_method=parsed.get("pickup_method"),
                pickup_date=parsed.get("pickup_date"),
                pickup_time=parsed.get("pickup_time"),
                extra_requirements=parsed.get("Extra_requirements")
            )
            session.add(order)

            # 更新訊息 used 標記
            session.query(Message).filter(Message.id.in_(message_ids)).update({"used": True}, synchronize_session=False)
            session.commit()

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="✅ 訂單已成功建立並儲存！感謝您！")
            )
            del session_order_cache[user_id]

        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"❌ 發生錯誤，請確認格式或稍後再試：{str(e)}")
            )

    session.close()

@app.route("/orders")
def orders():
    session = SessionLocal()
    orders = session.query(Order).all()
    data = []
    column_name = ["訂單ID", "姓名", "電話", "花材", "數量", "預算", "取貨方式", "取貨日期", "取貨時間", "備註"]

    for o in orders:
        user = session.query(User).filter_by(id=o.user_id).first()
        data.append({
            "id": o.id,
            "customer_name": user.customer_name if user else "未知",
            "phone": user.phone_number if user else "",
            "flower": o.flower_type,
            "qty": o.quantity,
            "budget": o.budget,
            "pickup_method": o.pickup_method,
            "pickup_date": o.pickup_date,
            "pickup_time": o.pickup_time,
            "note": o.extra_requirements
        })
    session.close()

    return render_template("orders.html", data=data, column_name=column_name)

import csv
from flask import Response

@app.route("/orders.csv")
def export_orders_csv():
    session = SessionLocal()
    orders = session.query(Order).all()
    output = []

    output.append([
        "訂單ID", "姓名", "電話", "花材", "數量", "預算", "取貨方式", "取貨日期", "取貨時間", "備註"
    ])

    for o in orders:
        user = session.query(User).filter_by(id=o.user_id).first()
        output.append([
            o.id,
            user.customer_name if user else "未知",
            user.phone_number if user else "",
            o.flower_type,
            o.quantity,
            o.budget,
            o.pickup_method,
            o.pickup_date,
            o.pickup_time,
            o.extra_requirements,
        ])
    session.close()

    def generate():
        for row in output:
            yield ",".join([str(col) for col in row]) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=orders.csv"}
    )

@app.route("/health")
def health():
    return "OK", 200

@app.route("/")
def index():
    return "Hello, this is the LINE bot server!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) # render deployment default port
    app.run(host="0.0.0.0", port=port, debug=True)
