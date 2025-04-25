# GPT Prompt 模板

import os

class PromptManager:
    def __init__(self, prompt_dir: str = "prompts"):
        """
        初始化 PromptManager，指定 prompt 檔案資料夾路徑。
        """
        self.prompt_dir = prompt_dir

    def load_prompt(self, name: str, **kwargs) -> str:
        """
        從指定名稱的 prompt 檔案讀取並填入參數。
        
        :param name: prompt 檔案名稱（不含 .txt）
        :param kwargs: 欲填入的參數，例如 user_message="..."
        :return: 填好參數的 prompt 字串
        """
        path = os.path.join(self.prompt_dir, f"{name}.txt")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Prompt file not found: {path}")

        with open(path, "r", encoding="utf-8") as file:
            template = file.read()

        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing parameter for prompt: {e}")

# 使用範例
if __name__ == "__main__":
    manager = PromptManager(prompt_dir="prompts")
    prompt = manager.load_prompt("order_prompt", user_message="我想訂兩束百合花，明天中午自取")
    print(prompt)
