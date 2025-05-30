<script setup>
import { ref, computed } from 'vue'
import { exportDocx, deleteOrder } from '@/api/orders'

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

const emit = defineEmits(['orderDeleted'])

// Add mapping between column names and data properties
const columnMapping = {
  '匯出工單': 'order_status',
  '訂單編號': 'id',
  '狀態': 'order_status',
  '取貨時間': 'send_datetime',
  '姓名': 'customer_name',
  '電話': 'customer_phone',
  '商品': 'item',
  '數量': 'quantity',
  '備註': 'note',
  '取貨方式': 'shipment_method',
  '金額': 'total_amount',
  '付款方式': 'pay_way',
  '付款狀態': 'pay_status',
  '取消訂單':'id'
}

const searchText = ref('')
const currentDate = ref(new Date())
const activeTab = ref('all')
const dateFilterActive = ref(false)

const formatDate = (date) => {
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  return `${date.getMonth() + 1} 月 ${date.getDate()} 日 (${weekdays[date.getDay()]})`
}

const goToPreviousDay = () => {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() - 1)
  currentDate.value = newDate
  dateFilterActive.value = true
  activeTab.value = ''
}

const goToNextDay = () => {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() + 1)
  currentDate.value = newDate
  dateFilterActive.value = true
  activeTab.value = ''
}

const formatDateTime = (datetime) => {
  if (!datetime) return ''
  const date = new Date(datetime)
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const year = date.getFullYear().toString().slice(-2)
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${year}/${month}/${day}（${weekdays[date.getDay()]}）${hours}:${minutes}`
}

// 狀態顏色對應
function statusColor(status) {
  switch (status) {
    case 'MANUAL': return 'badge-manual'
    case 'CONFIRMED': return 'badge-prepare'
    case 'FINISH': return 'badge-finish'
    default: return 'badge-manual'
  }
}

// 狀態文字對應
function statusText(status) { //改
  switch (status) {
    case 'MANUAL': return '人工溝通'
    case 'CONFIRMED': return '等待備貨'
    case 'FINISH': return '訂單完成'
    default: return status
  }
}

// 篩選符合搜尋文字與日期的訂單
const filteredData = computed(() => {
  if (!Array.isArray(props.data)) return []

  let result = props.data

  // 1. 先依activeTab篩選
  if (activeTab.value === 'manual') {
    result = result.filter(row => row.order_status === 'MANUAL')
  } else if (activeTab.value === 'prepare') {
    result = result.filter(row => row.order_status === 'CONFIRMED')
  } else if (activeTab.value === 'today') {
    // 今日訂單：依照currentDate
    const todayStr = currentDate.value.toISOString().slice(0, 10)
    result = result.filter(row => {
      if (!row.send_datetime) return false
      const rowDate = new Date(row.send_datetime).toISOString().slice(0, 10)
      return rowDate === todayStr
    })
  }

  // 2. 日期篩選（data-filter）
  if (dateFilterActive.value) {
    const filterStr = currentDate.value.toISOString().slice(0, 10)
    result = result.filter(row => {
      if (!row.send_datetime) return false
      const rowDate = new Date(row.send_datetime).toISOString().slice(0, 10)
      return rowDate === filterStr
    })
  }

  // 3. 搜尋文字
  if (searchText.value) {
    result = result.filter(row =>
      Object.values(row || {}).some(value =>
        String(value).toLowerCase().includes(searchText.value.toLowerCase())
      )
    )
  }
  return result
})

// 匯出成 CSV 檔案
function downloadCSV() {
  const headers = props.columnName
  const rows = props.data.map(row => [
    row.order_status,
    row.id,
    row.order_status,
    row.send_datetime,
    // new Date(row.send_datetime).toLocaleString(),
    row.customer_name,
    row.customer_phone,
    row.item,
    row.quantity,
    row.note,
    row.shipment_method === 'store_pickup' ? '店取' : '外送',
    row.total_amount,
    row.pay_way,
    row.pay_status,
    row.id
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

const handleExportDocx = async (orderId) => {
  try {
    const blob = await exportDocx(orderId)
    // Create a download link
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `order_${orderId}.docx`)
    document.body.appendChild(link)
    link.click()
    // Clean up
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Error exporting docx:', error)
    alert('匯出工單失敗: ' + error.message)
  }
}

const handleCancelOrder = async (orderId) => {
  try {
    await deleteOrder(orderId)
    // Show success message
    alert('訂單已成功取消')
    // Emit event to refresh the order list
    emit('orderDeleted', orderId)
  } catch (error) {
    console.error('Error canceling order:', error)
    alert('取消訂單時發生錯誤：' + (error.response?.data?.detail || error.message))
  }
}

const columnWidths = {
  '訂單編號': '136px',
  '狀態': '120px',
  '取貨時間': '200px',
  '姓名': '96px',
  '電話': '112px',
  '商品': '96px',
  '數量': '96px',
  '備註': '128px',
  '取貨方式': '128px',
  '金額': '96px',
  '付款方式': '128px',
  '付款狀態': '112px',
  '取消訂單':'96px' 
}

// 點擊日期filter按鈕時觸發
function onDateFilterClick() {
  dateFilterActive.value = true
  activeTab.value = '' // 取消tab篩選
}

// 點擊訂單總覽時觸發
function onOrderTitleClick() {
  dateFilterActive.value = false
  activeTab.value = 'all'
}
</script>

<template>
  <div class="section" id="orders">
    <div class="order-title-row">
      <span class="order-title" @click="onOrderTitleClick" style="cursor:pointer;">訂單總覽</span>
    </div>
    <div class="order-filter-row">
      <div class="order-tabs">
        <button 
          class="tab" 
          :class="{ active: activeTab === 'all' }"
          @click="activeTab = 'all'; dateFilterActive = false;"
        >所有訂單</button>
        <button 
          class="tab" 
          :class="{ active: activeTab === 'manual' }"
          @click="activeTab = 'manual'; dateFilterActive = false;"
        >人工溝通</button>
        <button 
          class="tab" 
          :class="{ active: activeTab === 'today' }"
          @click="activeTab = 'today'; dateFilterActive = false;"
        >今日訂單</button>
        <button 
          class="tab" 
          :class="{ active: activeTab === 'prepare' }"
          @click="activeTab = 'prepare'; dateFilterActive = false;"
        >等待備貨</button>
      </div>
      <div class="date-filter">
        <button class="date-nav-btn" @click="goToPreviousDay">
          <span class="arrow">&#60;</span>
        </button>
        <div class="current-date" @click="onDateFilterClick" :style="{cursor:'pointer', fontWeight: dateFilterActive ? 'bold' : 'normal', color: dateFilterActive ? '#6168FC' : ''}">{{ formatDate(currentDate) }}</div>
        <button class="date-nav-btn" @click="goToNextDay">
          <span class="arrow">&#62;</span>
        </button>
      </div>
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
        <i class="fas fa-download"></i>
        <span>下載 CSV</span>
      </button>
    </div>
    <div class="table-container">
      <div class="table-wrapper">
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th v-for="column in columnName" :key="column" :style="{ width: columnWidths[column] }">
                {{ column }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in filteredData" :key="index">
              <td v-for="column in columnName" :key="column" :style="{ width: columnWidths[column] }">
                <template v-if="column === '匯出工單'">
                  <button class="work-order-btn" @click="handleExportDocx(row.id)">工單</button>
                </template>
                <template v-else-if="column === '取消訂單'">
                  <button class="cancel-order-btn" @click="handleCancelOrder(row.id)">刪除</button>
                </template>
                <template v-else-if="column === '取貨時間'">
                  {{ formatDateTime(row[columnMapping[column]]) }}
                </template>
                <template v-else-if="column === '取貨方式'">
                  {{ row[columnMapping[column]] === 'store_pickup' ? '店取' : '外送' }}
                </template>
                <template v-else-if="column === '狀態'">
                  <span :class="['status-badge', statusColor(row[columnMapping[column]])]">
                    {{ statusText(row[columnMapping[column]]) }}
                  </span>
                </template>
                <template v-else>
                  {{ row[columnMapping[column]] }}
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
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
  padding-top: 24px;
  padding-bottom: 24px;
  padding-left: 32px;
  padding-right: 32px;
  margin-top: 24px;
  margin-bottom: 32px;
  border-bottom: 1.5px solid #e9e9e9;
}
.order-title-row {
  width: 100%;
  margin-bottom: 8px;
}
.order-title {
  color: #4F51FF;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 1px;
  white-space: nowrap;
}
.order-filter-row {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: nowrap;
  width: 100%;
  margin-bottom: 16px;
}
.order-tabs {
  display: inline-flex;
  gap: 4px;
  padding: 6px 12px;
  background: #F7F7F7;
  border-radius: 36px;
  height: 40px;
  align-items: center;
  flex-shrink: 0;
}
.tab {
  display: flex;
  align-items: center;
  padding: 11px 24px;
  height: 28px;
  border-radius: 36px;
  border: none;
  background: transparent;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 14px;
  line-height: 112.5%;
  color: rgba(0, 0, 0, 0.6);
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  flex-shrink: 0;
}
.tab.active {
  background: #C5C7FF;
  border-radius: 36px;
}
.date-filter {
  width: 203px;
  height: 28px;
  display: flex;
  align-items: center;
  padding: 11px 24px;
  gap: 8px;
  border-radius: 36px;
  background: #F7F7F7;
}
.search-group {
  position: relative;
  width: 360px;
  min-width: 360px;
  height: 46px;
  background: #D8EAFF;
  border-radius: 36px;
  display: flex;
  align-items: center;
  padding: 11px 24px;
}
.search-input {
  width: 100%;
  border: none;
  background: transparent;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 400;
  font-size: 16px;
  line-height: 140%;
  color: rgba(0, 0, 0, 0.38);
  padding: 0;
}
.search-input::placeholder {
  color: rgba(0, 0, 0, 0.38);
}
.search-icon {
  position: absolute;
  right: 24px;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  color: rgba(0, 0, 0, 0.38);
}
.download-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 12px;
  width: 113px;
  height: 46px;
  background: #77B5FF;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.25);
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  gap: 8px;
  white-space: nowrap;
}
.download-btn i {
  color: #FFFFFF;
  font-size: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
}
.download-btn span {
  font-family: 'Noto Sans TC', sans-serif;
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 112.5%;
  color: #FFFFFF;
  white-space: nowrap;
  flex: none;
  order: 1;
  flex-grow: 0;
  width: 66px;
  height: 18px;
  display: flex;
  align-items: center;
}
.table-container {
  margin-top: 0;
  width: 100%;
  overflow: hidden;
}

.table-wrapper {
  width: 100%;
  overflow-x: auto;
  padding: 0 8px;
}

table {
  border-collapse: separate;
  border-spacing: 0 8px;
  width: max-content;
  min-width: 100%;
}

thead {
  position: sticky;
  top: 0;
  z-index: 1;
}

th {
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: bold;
  font-size: 16px;
  line-height: 140%;
  color: rgba(0, 0, 0, 0.87);
  padding: 12px 20px;
  text-align: left;
  background-color: #F7F7F7;
  white-space: nowrap;
  position: relative;
  border: 0.5px solid rgba(175, 175, 175, 0.6);
}

th:first-child {
  border-top-left-radius: 12px;
  border-bottom-left-radius: 12px;
  border-right: none;
}

th:last-child {
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
  border-left: none;
}

th:not(:first-child):not(:last-child) {
  border-right: none;
  border-left: none;
}

td {
  padding: 12px 20px;
  text-align: left;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: bold;
  font-size: 16px;
  line-height: 140%;
  color: rgba(0, 0, 0, 0.6);
  vertical-align: middle;
  white-space: normal;
  word-wrap: break-word;
  max-width: v-bind('columnWidths[column]');
  background: #fff;
  border: 0.5px solid rgba(175, 175, 175, 0.6);
}

tr {
  background: #fff;
  border-radius: 12px;
}

td:first-child {
  border-top-left-radius: 12px;
  border-bottom-left-radius: 12px;
  border-right: none;
}

td:last-child {
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
  border-left: none;
}

td:not(:first-child):not(:last-child) {
  border-right: none;
  border-left: none;
}

tr:hover td {
  background-color: #f0f6ff;
}

.status-badge {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 6px 16px;
  gap: 10px;
  height: 28px;
  border-radius: 8px;
  font-family: 'Noto Sans TC', sans-serif;
  font-style: normal;
  font-weight: 700;
  font-size: 14px;
  line-height: 112.5%;
  text-align: center;
  white-space: nowrap;
}

.badge-manual {
  background: #FFCEE7;
  color: #FF349A;
}

.badge-prepare {
  background: #C5C7FF;
  color: #6168FC;
}

.badge-finish {
  background: #EBCDCC;
  color: #81386A;
}

.badge-download {
  background: #77B5FF;
  color: #FFFFFF;
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
.date-filter {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 16px;
  height: 40px;
  background: #F7F7F7;
  border-radius: 36px;
  margin: 0 8px;
}

.date-nav-btn {
  background: #D9D9D9;
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
  padding: 0;
}

.date-nav-btn:hover {
  background: #C5C7FF;
}

.arrow {
  font-size: 14px;
  font-weight: bold;
  line-height: 1;
}

.current-date {
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 14px;
  line-height: 112.5%;
  color: rgba(0, 0, 0, 0.6);
  min-width: 80px;
  text-align: center;
}

.work-order-btn {
  /* Auto layout */
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 6px 16px;
  gap: 10px;

  width: 60px;
  max-width: 92px;
  height: 28px;

  /* Secondary/Default */
  background: #77B5FF;
  border-radius: 8px;

  /* Inside auto layout */
  flex: none;
  order: 0;
  flex-grow: 0;

  /* Text styling */
  font-family: 'Noto Sans TC', sans-serif;
  font-style: normal;
  font-weight: 700;
  font-size: 14px;
  line-height: 112.5%;
  color: #FFFFFF;
  text-align: center;

  /* Button reset */
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.work-order-btn:hover {
  opacity: 0.8;
}

.cancel-order-btn {
  /* Auto layout */
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 6px 16px;
  gap: 10px;

  width: 60px;
  max-width: 92px;
  height: 28px;

  /* Alert/Default */
  background: #AE1914;
  border-radius: 8px;

  /* Inside auto layout */
  flex: none;
  order: 0;
  flex-grow: 0;

  /* Text styling */
  font-family: 'Noto Sans TC', sans-serif;
  font-style: normal;
  font-weight: 700;
  font-size: 14px;
  line-height: 112.5%;
  color: #EBCDCC;
  text-align: center;

  /* Button reset */
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.cancel-order-btn:hover {
  opacity: 0.8;
}
</style>


