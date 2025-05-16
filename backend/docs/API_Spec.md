# 📘 API 文件：花店自動化系統

本文件整理所有後端 API（Flask）設計與用途，供前端與後端開發與串接參考。

---

## 🟢 A. 前台（LINE Bot 自動對話流程）

### 3. 查詢和修改訂單草稿狀態

* **GET** `/api/draft-status?room_id=123`
* 回傳：是否已完成草稿與目前進度。

### 6. 確認送出訂單

* **POST** `/api/confirm-order`
* 根據草稿內容建立正式訂單、付款與出貨資訊。


### 10. 將 order 改成支援付款紀錄

* **POST** `/api/payments`

### 11. 更新訂單狀態

* **PATCH** `/api/orders/<id>`

## 🟡 C. 管理與設定

### 13. 查詢所有付款方式

* **GET** `/api/payment-methods`

### 14. 新增付款方式

* **POST** `/api/payment-methods`

### 15. 啟用 / 停用付款方式

* **PATCH** `/api/payment-methods/<id>`

### 訊息增加 is read 的欄位