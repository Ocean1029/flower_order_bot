from openai import OpenAI
import os
import json
from app.managers.prompt_manager import PromptManager
from dotenv import load_dotenv

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt_manager = PromptManager()

text = "我想要買一個包包"
gpt_prompt = prompt_manager.load_prompt("order_prompt", user_message=text)

response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "system", "content": gpt_prompt}],
            temperature=0
        )

gpt_reply = response.choices[0].message.content.strip()

print(gpt_reply)