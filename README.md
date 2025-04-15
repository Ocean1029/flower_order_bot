# Flower Shop Order Chatbot

本專案為一個花店訂單生成助手，透過 LINE Bot 將顧客訊息利用 OpenAI API 整理成格式化的訂單資訊（例如顧客姓名、聯絡電話、花材種類、數量、取貨時間及特殊需求）回傳給使用者。商家確認無誤後，資料將會被寫入訂單資料庫中，並可透過 `/orders` 頁面查詢所有訂單，也可經由 `/orders.csv` 匯出成表單，協助商家省下人工抄寫與反覆確認的時間成本。

目前專案已實作：
- ✅ 支援 LINE Bot 接收訊息、自動儲存使用者對話內容
- ✅ 使用 GPT 模型將對話轉換為結構化訂單（可控鍵觸發）
- ✅ 寫入 SQLite 或 Render PostgreSQL（依環境自動切換）
- ✅ 管理訂單、使用者資料與歷史訊息
- ✅ 提供 `/orders` 頁面檢視訂單與 `/orders.csv` 匯出下載
- ✅ 健康檢查頁 `/health` 適用 Render 或監控工具

---

## 📁 目錄
- [系統需求](#系統需求)
- [安裝與設定](#安裝與設定)
- [環境變數設定](#環境變數設定)
- [執行應用程式](#執行應用程式)
- [Webhook 配置](#webhook-配置)
- [程式架構說明](#程式架構說明)
- [專案目錄結構](#專案目錄結構)
- [授權](#授權)

---

## ✅ 系統需求
- 作業系統：MacOS / Linux / Windows
- Python：版本 3.8 或以上

---

## ⚙️ 安裝與設定

### 1. 複製專案
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. 建立虛擬環境
```bash
python3 -m venv venv
source venv/bin/activate  # Windows 為 venv\Scripts\activate
```

### 3. 安裝套件
```bash
pip install -r requirements.txt
```

---

## 🔐 環境變數設定
請在根目錄下建立 `.env` 檔案，內容如下：

```dotenv
OPENAI_API_KEY=你的 OpenAI 金鑰
LINE_CHANNEL_ACCESS_TOKEN=你的 LINE Bot Access Token
LINE_CHANNEL_SECRET=你的 LINE Channel Secret
```

> 可從 [OpenAI Platform](https://platform.openai.com/account/api-keys) 與 [LINE Developers](https://developers.line.biz/) 取得金鑰

---

## 🚀 執行應用程式

### 本地測試（開發）
```bash
python app.py
```                                                                                         
啟動後服務會運行於 `http://localhost:8000`

> 若搭配 [ngrok](https://ngrok.com) 可將 localhost 暴露給 LINE Webhook：
```bash
ngrok http 8000
```

### Render 雲端部署（正式）
- 上傳專案至 GitHub
- 在 Render 建立 Web Service（連接該 repo）
- 設定環境變數、Start Command：
```
gunicorn app:app
```

---

## 🔗 Webhook 配置
在 [LINE Developers Console](https://developers.line.biz/console/) 將 Webhook URL 設定為：

```
https://your-domain.onrender.com/callback
```

---

## 🧠 程式架構說明

### app.py
- 主啟動程式，匯入並註冊路由模組與資料模型

### models/
- `user.py`：User Model，含姓名、電話、LINE ID
- `order.py`：Order Model，訂單主資料
- `message.py`：儲存用戶對話紀錄，標記是否已處理
- `__init__.py`：統一管理 DB engine 與 Session

### routes/
- `linebot.py`：處理 LINE message webhook、GPT 整理邏輯、資料寫入
- `orders.py`：提供 `/orders`（頁面）與 `/orders.csv`（匯出）
- `health.py`：簡易 `GET /health` endpoint（給 Render/UptimeRobot 使用）

### templates/
- `orders.html`：訂單顯示頁面

---

## 📄 授權
本專案採用 MIT License，歡迎自由修改與商用。

---
