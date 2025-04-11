# Flower Shop Order Chatbot

本專案為一個花店訂單生成助手，讓他可以在商家與使用者的對話中解析出訂單詳情（例如顧客姓名、聯絡電話、花材種類、顏色、數量、取貨時間及特殊需求），並以 JSON 格式回傳給使用者。

---

## 目錄
- [Flower Shop Order Chatbot](#flower-shop-order-chatbot)
  - [目錄](#目錄)
  - [系統需求](#系統需求)
  - [安裝與設定](#安裝與設定)
    - [1. 複製專案至本地端](#1-複製專案至本地端)
    - [2. 建立虛擬環境（推薦步驟）](#2-建立虛擬環境推薦步驟)
    - [3. 安裝必要套件](#3-安裝必要套件)
  - [環境變數設定](#環境變數設定)
  - [執行應用程式](#執行應用程式)
  - [Webhook 配置](#webhook-配置)
  - [程式碼說明](#程式碼說明)
    - [核心檔案：`app.py`](#核心檔案apppy)
  - [授權](#授權)
  - [附錄](#附錄)

---
## 系統需求
- **作業系統：** MacOS (此專案亦可在其他作業系統上運行)
- **程式語言：** Python 3.7 或更新版本

---

## 安裝與設定

### 1. 複製專案至本地端
請利用 Git 指令或手動下載壓縮檔：
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. 建立虛擬環境（推薦步驟）
建立及啟用虛擬環境，以避免全域套件衝突：
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安裝必要套件
利用 pip 安裝 `requirements.txt` 中列舉的所有套件：
```bash
pip install -r requirements.txt
```

---

## 環境變數設定
請在專案根目錄下建立 `.env` 檔案，並加入以下內容：
```dotenv
OPENAI_API_KEY=你的OpenAI_API金鑰
LINE_CHANNEL_ACCESS_TOKEN=你的LINE渠道存取令牌
LINE_CHANNEL_SECRET=你的LINE渠道密鑰
```
此設定將使程式能夠正確讀取 OpenAI 與 LINE Bot 所需的金鑰與密鑰。
LINE CHANNEL ACCESS 可以從 http://manager.line.biz/ 註冊
OPEN API KEY 可以從 https://platform.openai.com/docs/overview 註冊

---

## 執行應用程式
完成上述設定後，可透過以下指令啟動 Flask 應用程式：
```bash
python app.py
```
程式預設運行於 `localhost:8000`，並且處於 debug 模式，利於開發與除錯。

---

## Webhook 配置
在 LINE Developer Console 中，將 Webhook URL 設定為：
```
http://<your-domain-or-ip>:8000/callback
```
若您於本地開發環境進行測試，建議使用 [ngrok](https://ngrok.com/) 等工具建立一個公開隧道，方便 LINE 伺服器存取您的應用程式。

---

## 程式碼說明

### 核心檔案：`app.py`
- **環境變數載入：**  
  透過 `dotenv` 套件從 `.env` 檔案中讀取 API 金鑰與其他敏感資訊。
  
- **LINE Bot API 整合：**  
  使用 `line-bot-sdk` 設定 LineBotApi 與 WebhookHandler，並透過 `/callback` 路由來接收及處理 LINE 平台所傳送的訊息。

- **OpenAI GPT 模型調用：**  
  定義一個包含訂單生成提示模板（`PROMPT_TEMPLATE`）的 prompt，並在接收到訊息後，利用 `openai_client.chat.completions.create()` 方法呼叫 GPT-3.5-turbo 模型，產生所需的訂單資訊。

- **訊息回覆：**  
  將從 GPT 模型得到的 JSON 格式訂單資訊，整合進回覆訊息中，並利用 `line_bot_api.reply_message()` 方法回傳給使用者。

---

## 授權
本專案遵循 MIT License 授權條款，詳細內容請參考專案中的 LICENSE 檔案。

---

## 附錄
- **修改與擴充：**  
  若需要調整訂單生成的流程或擴充其他功能，可參考 `PROMPT_TEMPLATE` 模板內容或進行 LINE Bot 的訊息格式修改。
- **進一步參考：**  
  請參考各套件官方文件以取得更多資訊：
  - [Flask](https://flask.palletsprojects.com/)
  - [python-dotenv](https://pypi.org/project/python-dotenv/)
  - [LINE Messaging API](https://developers.line.biz/)
  - [OpenAI API](https://platform.openai.com/docs/)
