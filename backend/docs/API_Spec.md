# 📘 API 文件：花店自動化系統

本文件整理所有後端 API（Flask）設計與用途，供前端與後端開發與串接參考。

---

## 🟢 A. 前台（LINE Bot 自動對話流程）

### 1. 接收 LINE Webhook

* **POST** `/callback`
* 接收 LINE 的訊息與互動事件，包含使用者輸入與按鈕回覆。

### 2. 取得聊天室訊息

* **GET** `/api/messages?room_id=123`
* 回傳：該聊天室的訊息列表。

```json
[
  {
    "direction": "incoming",
    "text": "我要買花",
    "time": "2025-05-11 10:33"
  },
  ...
]
```

### 3. 查詢訂單草稿狀態

* **GET** `/api/draft-status?room_id=123`
* 回傳：是否已完成草稿與目前進度。

### 4. 發送訊息至 LINE

* **POST** `/api/send-message`
* Body：

```json
{
  "room_id": 123,
  "text": "請問取貨時間？"
}
```

### 5. 建立訂單草稿

* **POST** `/api/draft-order`
* 由 Bot 整理後提交 JSON 結果。

### 6. 確認送出訂單

* **POST** `/api/confirm-order`
* 根據草稿內容建立正式訂單、付款與出貨資訊。

---

## 🔵 B. 後台（店家管理用）

### 7. 取得聊天室預覽（Dashboard）

* **GET** `/api/stats`
* 回傳：所有聊天室與其最新訊息。

### 8. 查詢所有訂單

* **GET** `/api/orders`
* 回傳：訂單列表，含使用者資訊與訂單狀態。

### 9. 查詢單一訂單

* **GET** `/api/orders/<id>`

### 10. 建立付款紀錄

* **POST** `/api/payments`

```json
{
  "order_id": 1,
  "amount": 1500,
  "method_id": 2,
  "screenshot_url": "https://..."
}
```

### 11. 更新訂單狀態

* **PATCH** `/api/orders/<id>`

```json
{
  "status": "confirmed"
}
```

### 12. 修改使用者資訊

* **PATCH** `/api/users/<id>`

```json
{
  "name": "張三",
  "phone": "0912xxxxxx"
}
```

---

## 🟡 C. 管理與設定

### 13. 查詢所有付款方式

* **GET** `/api/payment-methods`

### 14. 新增付款方式

* **POST** `/api/payment-methods`

### 15. 啟用 / 停用付款方式

* **PATCH** `/api/payment-methods/<id>`

```json
{
  "active": false
}
```

### 16. 查詢通知紀錄

* **GET** `/api/notifications`

---

## 🧪 附註

* 建議使用者登入（staff）之後，才可存取後台 API
* 訊息與訂單資料皆會保留 timestamp，用於排序與查詢
