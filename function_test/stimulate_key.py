import hmac
import hashlib
import base64
import os
from dotenv import load_dotenv

load_dotenv()
# 讀取環境變數
channel_secret = os.getenv("LINE_CHANNEL_SECRET")

# 請將此處的 request_body 修改成你在 Postman 使用的完整原始 JSON 字串（二進位）
request_body = '''{
  "events": [
    {
      "replyToken": "dummy_reply_token",
      "type": "message",
      "timestamp": 1615325590000,
      "source": {
        "type": "user",
        "userId": "dummy_user_id"
      },
      "message": {
        "id": "dummy_message_id",
        "type": "text",
        "text": "訂購花束，姓名：張三，電話：0987654321，花材種類：玫瑰，顏色：紅色，數量：3束，取貨時間：2025-04-12 14:00"
      }
    }
  ]
}'''

# 將 request_body 轉換為位元組
request_body = request_body.encode('utf-8')

# 使用 HMAC-SHA256 計算雜湊值
hash = hmac.new(channel_secret.encode('utf-8'), request_body, hashlib.sha256).digest()

# 將雜湊值以 Base64 編碼，產生簽章字串
signature = base64.b64encode(hash).decode('utf-8')

print("X-Line-Signature:", signature)
