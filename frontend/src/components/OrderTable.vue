<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  columnName: {
    type: Array,
    required: true
  }
})

const searchText = ref('')

// 狀態顏色對應
function statusColor(status) {
  switch (status) {
    case 'pending': return 'badge-blue'
    case 'confirmed': return 'badge-pink'
    case 'cancelled': return 'badge-gray'
    case 'completed': return 'badge-brown'
    default: return 'badge-gray'
  }
}

// 篩選符合搜尋文字的訂單
const filteredData = computed(() => {
  if (!Array.isArray(props.data)) return []
  
  if (!searchText.value) return props.data
  
  return props.data.filter(row =>
    Object.values(row || {}).some(value =>
      String(value).toLowerCase().includes(searchText.value.toLowerCase())
    )
  )
})

// 匯出成 CSV 檔案
function downloadCSV() {
  const headers = props.columnName
  const rows = props.data.map(row => [
    row.id,
    row.customer_name,
    row.customer_phone,
    row.receipt_address,
    new Date(row.order_date).toLocaleString(),
    row.total_amount,
    row.item,
    row.quantity,
    row.note,
    row.pay_way,
    row.card_message,
    row.weekday,
    new Date(row.send_datetime).toLocaleString(),
    row.receiver_name,
    row.receiver_phone,
    row.delivery_address,
    row.order_status,
    row.shipment_method === 'store_pickup' ? '店取' : '外送'
  ])

  const csvContent = [headers, ...rows]
    .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
    .join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', '訂單資料.csv')
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<template>
  <div class="section" id="orders">
    <div class="header">
      <span class="order-title">訂單總覽</span>
    </div>
    <!-- 分類 bar -->
    <div class="order-tabs">
      <button class="tab active">所有訂單</button>
      <button class="tab">人工溝通</button>
      <button class="tab">今日訂單</button>
      <button class="tab">等待備貨</button>
      <button class="tab">錯誤訊息</button>
    </div>
    <!-- 搜尋與下載 -->
    <div class="order-search-row">
      <div class="search-group">
        <input
          type="text"
          v-model="searchText"
          class="search-input"
          placeholder="搜尋訂單（姓名、編號等）"
        />
        <span class="search-icon"><i class="fas fa-search"></i></span>
      </div>
      <button @click="downloadCSV" class="download-btn">
        <i class="fas fa-download"></i> 下載 CSV
      </button>
    </div>
    <div class="table-container table-responsive">
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th>訂單ID</th>
            <th>客戶姓名</th>
            <th>客戶電話</th>
            <th>收件地址</th>
            <th>訂單日期</th>
            <th>總金額</th>
            <th>商品</th>
            <th>數量</th>
            <th>備註</th>
            <th>付款方式</th>
            <th>卡片訊息</th>
            <th>星期</th>
            <th>送貨日期時間</th>
            <th>收件人姓名</th>
            <th>收件人電話</th>
            <th>送貨地址</th>
            <th>訂單狀態</th>
            <th>送貨方式</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in filteredData" :key="index">
            <td>{{ row.id }}</td>
            <td>{{ row.customer_name }}</td>
            <td>{{ row.customer_phone }}</td>
            <td>{{ row.receipt_address }}</td>
            <td>{{ new Date(row.order_date).toLocaleString() }}</td>
            <td><span class="money">NT {{ row.total_amount }}</span></td>
            <td>{{ row.item }}</td>
            <td>{{ row.quantity }}</td>
            <td>{{ row.note }}</td>
            <td>{{ row.pay_way }}</td>
            <td>{{ row.card_message }}</td>
            <td>{{ row.weekday }}</td>
            <td>{{ new Date(row.send_datetime).toLocaleString() }}</td>
            <td>{{ row.receiver_name }}</td>
            <td>{{ row.receiver_phone }}</td>
            <td>{{ row.delivery_address }}</td>
            <td>
              <span :class="['status-badge', statusColor(row.order_status)]">
                {{ row.order_status === 'confirmed' ? '已確認' : row.order_status }}
              </span>
            </td>
            <td>{{ row.shipment_method === 'store_pickup' ? '店取' : '外送' }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="filteredData.length === 0" class="no-results">
        <i class="fas fa-search fa-2x mb-3"></i>
        <p>找不到符合條件的訂單</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.section {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 32px;
  border-bottom: 1.5px solid #e9e9e9;
}
.header {
  margin-bottom: 0;
  
}
.order-title {
  color: #4F51FF;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 1px;
  
}
.order-tabs {
  display: flex;
  gap: 12px;
  margin: 18px 0 18px 0;
}
.tab {
  background: #f5f6fa;
  color: #7B61FF;
  border: none;
  border-radius: 8px 8px 0 0;
  padding: 8px 22px;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.tab.active {
  background: #eaf2ff;
  color: #4F8CFF;
}
.order-search-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
  gap: 16px;
}
.search-group {
  position: relative;
  width: 340px;
}
.search-input {
  width: 100%;
  padding: 10px 44px 10px 18px;
  border-radius: 8px;
  border: 1.5px solid #eaf2ff;
  background: #f5f6fa;
  font-size: 16px;
  font-weight: 500;
}
.search-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #A3C8FF;
  font-size: 18px;
}
.download-btn {
  padding: 10px 20px;
  background: #4F8CFF;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  font-size: 16px;
  box-shadow: 0 2px 8px rgba(79,140,255,0.08);
  transition: background 0.2s;
}
.download-btn:hover {
  background: #007AFF;
}
.table-container {
  margin-top: 0;
}
th, td {
  padding: 14px 10px;
  text-align: left;
  border-bottom: 1.5px solid #e9e9e9;
  font-size: 15px;
  vertical-align: middle;
}
th {
  background-color: #f5f6fa;
  font-weight: 700;
  color: #7B61FF;
  font-size: 16px;
  letter-spacing: 1px;
}
tr:hover {
  background-color: #f0f6ff;
}
.status-badge {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
}
.badge-blue {
  background: #4F8CFF;
  color: #fff;
}
.badge-pink {
  background: #F8D7E7;
  color: #FF6F91;
}
.badge-purple {
  background: #E6E6FA;
  color: #7B61FF;
}
.badge-brown {
  background: #F5E6DE;
  color: #BCA37F;
}
.badge-gray {
  background: #bdbdbd;
  color: #fff;
}
.money {
  color: #4F8CFF;
  font-weight: bold;
  font-size: 16px;
}
.text-danger {
  color: #FF6F91;
  font-weight: bold;
}
.no-results {
  text-align: center;
  padding: 40px;
  color: #aaa;
}
</style>


