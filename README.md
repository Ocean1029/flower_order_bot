# Chi-Mei Floral

本專案為一個花店商家後台，透過 LINE Bot 將顧客訊息利用 OpenAI API 整理成格式化的訂單資訊（例如顧客姓名、聯絡電話、花材種類、數量、取貨時間及特殊需求）回傳給使用者。商家確認無誤後，資料將會被寫入訂單資料庫中，並可透過 `/orders` 頁面查詢所有訂單，也可經由 `/orders.csv` 匯出成表單，協助商家省下人工抄寫與反覆確認的時間成本。

---

## ✅ 已實作功能

* ✅ 支援 LINE Bot 接收訊息、自動儲存使用者對話內容
* ✅ 使用 GPT 模型將對話轉換為結構化訂單（透過關鍵字觸發）
* ✅ 寫入 SQLite（開發）或 Render PostgreSQL（部署）
* ✅ 管理訂單、顧客資料與歷史訊息
* ✅ 提供 `/orders` 頁面查詢訂單，並支援 `/orders.csv` 匯出
* ✅ 前端以 Vue 框架實作，可即時查看與操作訂單系統
* ✅ 使用 Alembic 作資料庫版本控制

---

## 📁 目錄

* [系統需求](#系統需求)
* [安裝與設定](#安裝與設定)
* [環境變數設定](#環境變數設定)
* [執行應用程式](#執行應用程式)
* [Webhook 配置](#webhook-配置)
* [程式架構說明](#程式架構說明)
* [專案目錄結構](#專案目錄結構)
* [授權](#授權)

---

## ⚙️ 系統需求

* 作業系統：MacOS / Linux / Windows
* Python：3.8 以上
* Node.js：18+（前端執行需使用）

---

## 🧰 安裝與設定

### 1. 複製專案

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. 建立虛擬環境（後端）

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows 用 venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 安裝前端依賴（Vue）

```bash
cd frontend
npm install
```

---

## 🔐 環境變數設定

請在專案 `backend` 目錄下建立 `.env` 檔案，可參考 .env.example 檔案。若需完全使用 LINE Bot 和 OpenAI 功能，他們的金鑰取得方式如下：

* [OpenAI Platform](https://platform.openai.com/account/api-keys)
* [LINE Developers Console](https://developers.line.biz/console/)

---

## 🚀 執行應用程式

### ✅ 開發模式（本地）

#### 後端

```bash
cd backend
uvicorn app.main:app --reload
```

啟動後預設運行於 `http://localhost:8000`

#### 前端

```bash
cd frontend
npm run dev
```

啟動後預設運行於 `http://localhost:5173`

#### 資料庫
```bash
cd backend
alembic upgrade head # 將資料表格式更新為最新版本
PYTHONPATH=. python app/seed/seed_all.py # 產生 10 筆測試資料進入 messages.db
```


> 📦 可使用 [ngrok](https://ngrok.com) 來將 localhost 對外暴露給 LINE Webhook：

```bash
ngrok http 8000
```

---

### 🌐 Render 雲端部署

#### 後端

1. 將專案上傳至 GitHub
2. 前往 [Render](https://render.com) 建立 Web Service
3. 設定：

   * 環境變數 `.env` 內容
   * Start Command:

     ```bash
     gunicorn app.main:app
     ```

#### 前端待捕

---

## 🔗 Webhook 配置

請至 [LINE Developers Console](https://developers.line.biz/console/) 設定 Webhook URL：

```
https://your-domain.onrender.com/callback
```

---

## 🧠 程式架構說明

### `backend/app/` 後端（FastAPI）

* `main.py`：主應用與路由掛載
* `models/`：資料表定義（User、Order、Message、Shipment 等）
* `routes/`：API 路由模組（linebot、orders、health 等）
* `services`：實作各種資料庫 CRUD 功能
* `schemas/`：定義資料 Input 與 Output 格式
* `core/`：資料庫設定與 Alembic 支援
* `seed/`：虛擬資料產生程式

### `frontend/` 前端（Vue）

* Vue 專案：提供聊天室介面、訂單列表等操作頁面
* 其他待捕
---

## 📄 授權 License

本專案採用 [MIT License](LICENSE)，歡迎自由使用、修改與商業應用。
