from openai import OpenAI
import os
import json
from app.managers.prompt_manager import PromptManager
from dotenv import load_dotenv
import datetime

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt_manager = PromptManager()

text = "我想要買一個包包"
draft = {
     "customer_name": "Benjamin",
     "customer_phone": "",
     "receiver_name": "",
     "receiver_phone": "",
     "order_date": "2025-04-20T00:00:00Z",
     "pay_way": "",
     "total_amount": -1,
     "item": "母親節超好笑限定花束",
     "quantity": -1,
     "note": "",
     "card_message": "",
     "shipment_method": "DELIVERY",
     "send_datetime": "2025-04-20T15:00:00Z",
     "receipt_address": "",
     "delivery_address": "台北市信義區市政府路45號"
   }
gpt_prompt = prompt_manager.load_prompt("order_prompt", user_message=text, order_draft=json.dumps(draft or {}))
print(gpt_prompt)

response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "system", "content": gpt_prompt}],
            temperature=0
        )

gpt_reply = response.choices[0].message.content.strip()

print("\n",gpt_reply)