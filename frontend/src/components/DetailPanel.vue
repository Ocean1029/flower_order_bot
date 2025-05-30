<template>
  <transition name="slide-detail">
    <div class="order-detail-panel">
      <!-- section: 最上方 bar -->
      <div class="section">
        <div class="head">
          <div class="text-group">
            <span class="section-title">訂單草稿</span>
            <div class="edit-btn" @click="isEditing ? confirmEditing() : startEditing()">
              <div class="press">
                <i v-if="!isEditing" class="fas fa-pen icon"></i>
                <i v-else class="fas fa-check icon"></i>
              </div>
            </div>
          </div>
          <div class="icon-block" @click="$emit('close-detail')">
            <div class="ellipse"></div>
            <i class="fas fa-angle-double-left chevrons-left"></i>
          </div>
        </div>
      </div>
      <div class="order-detail-content">
        <template v-for="(col, idx) in columns" :key="col">
          <template v-if="col === '送貨日期'">
            <!-- 第一行：標題+日期 -->
            <div class="table-row">
              <div class="table-column" :class="{ 'missing-field': isFieldMissing(col) }">{{ col }}</div>
              <div class="data-container">
                <template v-if="isEditing">
                  <input
                    type="date"
                    v-model="editedData[col + '_date']"
                    class="edit-input"
                    :class="{ 'missing-field-input': isFieldMissing(col) }"
                  />
                </template>
                <span v-else class="data" :class="{ 'missing-field': isFieldMissing(col) }">{{ dataList[idx] }}</span>
              </div>
            </div>
            <!-- 第二行：空白+時間 -->
            <div class="table-row">
              <div class="table-column"></div>
              <div class="data-container">
                <template v-if="isEditing">
                  <input
                    type="time"
                    v-model="editedData[col + '_time']"
                    class="edit-input"
                    :class="{ 'missing-field-input': isFieldMissing(col) }"
                    step="300"
                  />
                </template>
              </div>
            </div>
          </template>
          <template v-else>
            <!-- 其他欄位照舊 -->
            <div class="table-row">
              <div class="table-column" :class="{ 'missing-field': isFieldMissing(col) }">{{ col }}</div>
              <div class="data-container">
                <template v-if="isEditing && editableFields.includes(col)">
                  <select 
                    v-if="col === '取貨方式'"
                    v-model="editedData[col]"
                    class="edit-select"
                    :class="{ 'missing-field-input': isFieldMissing(col) }"
                    :ref="el => setInputRef(el, col)"
                    @keydown.enter.prevent="handleEnterKey(col)"
                  >
                    <option value="店取">店取</option>
                    <option value="外送">外送</option>
                  </select>
                  <input 
                    v-else
                    v-model="editedData[col]"
                    class="edit-input"
                    :class="{ 'missing-field-input': isFieldMissing(col) }"
                    type="text"
                    :ref="el => setInputRef(el, col)"
                    @keydown.enter.prevent="handleEnterKey(col)"
                  />
                </template>
                <span v-else class="data" :class="{ 'missing-field': isFieldMissing(col) }">{{ dataList[idx] }}</span>
              </div>
            </div>
          </template>
        </template>        
      </div>
      <!-- bottom: frame-2 兩個新按鈕 -->
      <div class="frame-2">
        <div class="order-btn update" :class="{ editing: isEditing }" @click="handleUpdateOrder">
          <i class="fas fa-upload btn-icon"></i>
          <span class="btn-text">更新工單</span>
        </div>
        <div class="order-btn create" :class="{ editing: isEditing }" @click="handleCreateOrder">
          <i class="fas fa-plus btn-icon"></i>
          <span class="btn-text">建立新工單</span>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { sendOrderDraft, createOrder_FromDraft, updateOrder } from '@/api/orders'

const props = defineProps({
  orderData: Object,
  roomId: String
})

const emit = defineEmits(['close-detail'])
const missingFields = ref([])

// 可編輯的欄位
const editableFields = [
  '客戶姓名', '客戶電話', '收件人姓名', '收件人電話', '總金額', '品項', '數量', '備註', 
  '卡片訊息', '取貨方式', '送貨日期', '收件地址', '送貨地址', '付款方式'
]

// 依照原本順序組成資料陣列
const columns = [
  '客戶姓名', '客戶電話', '收件人姓名', '收件人電話', '總金額', 
  '品項', '數量', '備註', '卡片訊息', '取貨方式', '送貨日期', '收件地址', 
  '送貨地址', '訂單日期', '付款方式', '星期'
]
const dataList = computed(() => [
  props.orderData?.customer_name || ' ',
  props.orderData?.customer_phone || ' ',
  props.orderData?.receiver_name || ' ',
  props.orderData?.receiver_phone || ' ',
  props.orderData?.total_amount ? 'NT ' + props.orderData.total_amount : ' ',
  props.orderData?.item || ' ',
  props.orderData?.quantity || ' ',
  props.orderData?.note || ' ',
  props.orderData?.card_message || ' ',
  props.orderData?.shipment_method === 'STORE_PICKUP' ? '店取' : '外送',
  formatDateTime(props.orderData?.send_datetime),
  props.orderData?.receipt_address || ' ',
  props.orderData?.delivery_address || ' ',
  formatDateTime(props.orderData?.order_date),
  props.orderData?.pay_way || ' ',
  props.orderData?.weekday || ' '
])

const isEditing = ref(false)
const editedData = ref({})

// 獲取所有可編輯欄位的索引
const editableIndices = computed(() => {
  return columns.reduce((indices, col, idx) => {
    if (editableFields.includes(col)) {
      indices.push(idx);
    }
    return indices;
  }, []);
});

// 用於存儲所有輸入框的引用
const inputRefs = ref({})

// 設置輸入框引用
function setInputRef(el, col) {
  if (el) {
    inputRefs.value[col] = el
  }
}

function formatDateTime(dateStr) {
  if (!dateStr) return ' '
  const date = new Date(dateStr)
  return date.toLocaleString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function startEditing() {
  isEditing.value = true
  // 初始化編輯數據
  columns.forEach((col, idx) => {
    if (editableFields.includes(col)) {
      if (col === '送貨日期') {
        const date = new Date(dataList.value[idx])
        editedData.value[col + '_date'] = date.toISOString().split('T')[0]
        editedData.value[col + '_time'] = date.toTimeString().slice(0, 5)
      } else {
        editedData.value[col] = dataList.value[idx]
      }
    }
  })
}

async function confirmEditing() {
  try {
    // Format the data according to the API requirements
    const orderDraftData = {
      customer_name: editedData.value['客戶姓名'] || '',
      customer_phone: editedData.value['客戶電話'] || '',
      receiver_name: editedData.value['收件人姓名'] || '',
      receiver_phone: editedData.value['收件人電話'] || '',
      total_amount: parseFloat(editedData.value['總金額']?.replace('NT ', '') || '0'),
      item: editedData.value['品項'] || '',
      quantity: parseInt(editedData.value['數量'] || '0'),
      note: editedData.value['備註'] || '',
      card_message: editedData.value['卡片訊息'] || '',
      shipment_method: editedData.value['取貨方式'] === '店取' ? 'STORE_PICKUP' : 'DELIVERY',
      send_datetime: editedData.value['送貨日期_date'] && editedData.value['送貨日期_time']
        ? new Date(`${editedData.value['送貨日期_date']}T${editedData.value['送貨日期_time']}`).toISOString().replace(/\.\d{3}Z$/, '.331Z')
        : new Date().toISOString().replace(/\.\d{3}Z$/, '.331Z'),
      receipt_address: editedData.value['收件地址'] || '',
      delivery_address: editedData.value['送貨地址'] || '',
      pay_way: editedData.value['付款方式'] || '',
      pay_way_id: 0 // You might want to map this to actual IDs
    }

    console.log('Sending order draft data:', orderDraftData)
    await sendOrderDraft(props.roomId, orderDraftData)
    
    isEditing.value = false
    editedData.value = {}
    
    // Emit an event to refresh the data
    emit('orderDraftUpdated')
  } catch (error) {
    console.error('Error updating order draft:', error)
    alert('更新訂單失敗: ' + error.message)
  }
}

async function handleCreateOrder() {
  try {
    if (!props.roomId) {
      throw new Error('No room ID provided')
    }

    // If in editing mode, save the draft first
    if (isEditing.value) {
      await confirmEditing()
    }

    // Create the order
    const response = await createOrder_FromDraft(props.roomId)
    console.log('Order created:', response)
    
    // Only show success message if response is null (successful creation)
    if (response == '') {
      alert('工單建立成功！')
      // Reset missing fields
      missingFields.value = []
      // Emit an event to refresh the data
      emit('orderDraftUpdated')
    } 
    else {
      // If response contains missing fields, show them
      alert('請填入缺少的資料')
      if (Array.isArray(response)) {
        missingFields.value = response
      }
    }
  } catch (error) {
    console.error('Error creating order:', error)
    // Check if the error response contains missing fields
    if (error.response?.data && Array.isArray(error.response.data)) {
      missingFields.value = error.response.data
    } else {
      alert('建立工單失敗: ' + error.message)
    }
  }
}

async function handleUpdateOrder() {
  try {
    if (!props.roomId) {
      throw new Error('No room ID provided')
    }

    // If in editing mode, save the draft first
    if (isEditing.value) {
      await confirmEditing()
    }

    // Format the data according to the API requirements
    const orderDraftData = {
      customer_name: editedData.value['客戶姓名'] || props.orderData?.customer_name || '',
      customer_phone: editedData.value['客戶電話'] || props.orderData?.customer_phone || '',
      receiver_name: editedData.value['收件人姓名'] || props.orderData?.receiver_name || '',
      receiver_phone: editedData.value['收件人電話'] || props.orderData?.receiver_phone || '',
      total_amount: parseFloat(editedData.value['總金額']?.replace('NT ', '') || props.orderData?.total_amount || '0'),
      item: editedData.value['品項'] || props.orderData?.item || '',
      quantity: parseInt(editedData.value['數量'] || props.orderData?.quantity || '0'),
      note: editedData.value['備註'] || props.orderData?.note || '',
      card_message: editedData.value['卡片訊息'] || props.orderData?.card_message || '',
      shipment_method: editedData.value['取貨方式'] === '店取' ? 'STORE_PICKUP' : 'DELIVERY',
      send_datetime: editedData.value['送貨日期_date'] && editedData.value['送貨日期_time']
        ? new Date(`${editedData.value['送貨日期_date']}T${editedData.value['送貨日期_time']}`).toISOString().replace(/\.\d{3}Z$/, '.331Z')
        : props.orderData?.send_datetime || new Date().toISOString().replace(/\.\d{3}Z$/, '.331Z'),
      receipt_address: editedData.value['收件地址'] || props.orderData?.receipt_address || '',
      delivery_address: editedData.value['送貨地址'] || props.orderData?.delivery_address || '',
      pay_way: editedData.value['付款方式'] || props.orderData?.pay_way || '',
      pay_way_id: 0
    }

    console.log('Updating order with data:', orderDraftData)
    await updateOrder(props.roomId, orderDraftData)
    
    alert('工單更新成功！')
    // Emit an event to refresh the data
    emit('orderDraftUpdated')
  } catch (error) {
    console.error('Error updating order:', error)
    alert('更新工單失敗: ' + error.message)
  }
}

// 處理 Enter 鍵事件
function handleEnterKey(currentCol) {
  const currentIndex = editableFields.indexOf(currentCol)
  if (currentIndex < editableFields.length - 1) {
    const nextCol = editableFields[currentIndex + 1]
    const nextInput = inputRefs.value[nextCol]
    if (nextInput) {
      nextTick(() => {
        nextInput.focus()
      })
    }
  }
}

// Add a function to check if a field is missing
function isFieldMissing(field) {
  const fieldMapping = {
    '數量': 'quantity',
    '總金額': 'total_amount',
    '品項': 'item',
    '客戶姓名': 'customer_name',
    '客戶電話': 'customer_phone',
    '收件人姓名': 'receiver_name',
    '收件人電話': 'receiver_phone',
    '取貨方式': 'shipment_method',
    '送貨日期': 'send_datetime',
    '收件地址': 'receipt_address',
    '送貨地址': 'delivery_address',
    '付款方式': 'pay_way'
  }
  return missingFields.value.includes(fieldMapping[field])
}
</script>

<style scoped>
.order-detail-panel {
  width: 336px;
  height: calc(100vh - 56px);
  position: fixed;
  top: 56px;
  right: 0;
  background: #fff;
  border-right: 1px solid #B3B3B3;
  display: flex;
  flex-direction: column;
  padding-bottom: 72px;
  scrollbar-width: thin;
  scrollbar-color: #E4E4E4 #F7F7F7;
}

.section {
  width: 336px;
  height: 80px;
  display: flex;
  align-items: center;  
  border-bottom: 1.5px solid #e9e9e9;
}

.head {
  width: 284px;
  height: 36px;
  top: 22px;
  margin-left: 26px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text-group {
  display: flex;
  align-items: center;
  width: 124px;
  height: 36px;
  gap: 16px;
}

.section-title {
  height: 25px;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 18px;
  line-height: 140%;
  letter-spacing: 0%;
  vertical-align: middle;
  color: #000000;
}

.edit-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.1s ease;
}

.edit-btn:active {
  transform: scale(0.95);
}

.press {
  width: 32px;
  height: 32px;
  background: #D9D9D9;
  border-radius: 50%;
  position: relative;
  top: 2px;
  left: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon {
  width: 18px;
  height: 18px;
  color: #6168FC;
  position: relative;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-block {
  width: 36px;
  height: 36px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: none;
  border: none;
  color: #528DD2;
  rotate: -180deg;
  transition: transform 0.1s ease;
}

.icon-block:active {
  transform: scale(0.95);
}

.ellipse {
  width: 32px;
  height: 32px;
  background: #D8EAFF;
  border-radius: 50%;
  position: absolute;
}

.chevrons-left {  
  width: 16;
  border: none;
  background: none;
  rotate: 0deg;
  background: transparent;
}

.order-detail-content {
  display: flex;
  flex-direction: column;
  padding: 24px;
  gap: 16px;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 120px;
}

.table-row {
  display: flex;
  align-items: center;
  height: 32px;
  gap: 8px;
}

.table-column {
  width: 110px;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 16px;
  line-height: 140%;
  color: #000000DE;
  background: none;
}

.data-container {
  flex: 1;
}

.data {
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 16px;
  line-height: 140%;
  color: #000;
  background: none;
  vertical-align: middle;
}

.edit-input,
.edit-select {
  width: 100%;
  padding: 8px 12px;
  border: 1.5px solid #e0e3ed;
  border-radius: 6px;
  background: #fafbff;
  color: #222;
  font-size: 15px;
  font-family: 'Noto Sans TC', sans-serif;
  transition: border 0.2s, box-shadow 0.2s;
  box-shadow: none;
  outline: none;
}

.edit-input:focus,
.edit-select:focus {
  border-color: #6168FC;
  box-shadow: 0 0 0 2px #e4e7ff;
}

.edit-input:active,
.edit-select:active {
  transform: scale(0.98);
}

/* 自訂下拉箭頭 */
.edit-select {
  background-image: url("data:image/svg+xml,%3Csvg width='16' height='16' fill='none' stroke='%236168FC' stroke-width='2' viewBox='0 0 24 24'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 18px 18px;
}

/* 日期、時間 input */
input[type='date'].edit-input,
input[type='time'].edit-input {
  width: 100%;
  padding: 8px 12px;
  border: 1.5px solid #e0e3ed;
  border-radius: 6px;
  background: #fafbff;
  color: #222;
  font-size: 15px;
  font-family: 'Noto Sans TC', sans-serif;
  transition: border 0.2s, box-shadow 0.2s;
  box-shadow: none;
  outline: none;
}

input[type='date'].edit-input:focus,
input[type='time'].edit-input:focus {
  border-color: #6168FC;
  box-shadow: 0 0 0 2px #e4e7ff;
}

input[type='date'].edit-input:active,
input[type='time'].edit-input:active {
  transform: scale(0.98);
}

/* 日曆、時鐘 icon 簡約化 */
input[type='date'].edit-input::-webkit-calendar-picker-indicator,
input[type='time'].edit-input::-webkit-calendar-picker-indicator {
  filter: invert(38%) sepia(98%) saturate(747%) hue-rotate(202deg) brightness(97%) contrast(92%);
  opacity: 0.7;
  transition: opacity 0.2s;
  cursor: pointer;
}

input[type='date'].edit-input:focus::-webkit-calendar-picker-indicator,
input[type='time'].edit-input:focus::-webkit-calendar-picker-indicator {
  opacity: 1;
}

.delivery-time-inputs {
  display: flex;
  gap: 8px;
  flex: 1;
}

.delivery-time-inputs input {
  flex: 1;
  height: 32px;
  padding: 4px 8px;
  border: 1.5px solid #e9e9e9;
  border-radius: 4px;
  font-size: 14px;
  font-family: 'Noto Sans TC', sans-serif;
  transition: all 0.1s ease;
  background-color: white;
  color: #000;
}

.delivery-time-inputs input:active {
  transform: scale(0.98);
}

.delivery-time-inputs input:focus {
  border-color: #6168FC;
  outline: none;
  box-shadow: 0 0 0 2px rgba(97, 104, 252, 0.1);
}

.delivery-time-inputs input[type="date"]::-webkit-calendar-picker-indicator,
.delivery-time-inputs input[type="time"]::-webkit-calendar-picker-indicator {
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
  padding: 0;
  margin: 0;
}

.delivery-time-inputs input[type="date"]::-webkit-calendar-picker-indicator:hover,
.delivery-time-inputs input[type="time"]::-webkit-calendar-picker-indicator:hover {
  opacity: 1;
}

.frame-2 {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 16px;
  display: flex;
  gap: 8px;
  justify-content: center;
  z-index: 20;
}
.order-btn {
  width: 136px;
  height: 40px;
  border-radius: 12px;
  padding: 12px 12px;
  box-shadow: 2px 2px 2px 0px #00000040;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: #77B5FF;
  transition: all 0.1s ease;
  border: none !important;
  outline: none !important;
}
.order-btn:active {
  transform: scale(0.95);
  box-shadow: 1px 1px 1px 0px #00000040;
}
.order-btn.editing {
  background: #C5C7FF;
}
.btn-icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-text {
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 16px;
  line-height: 113%;
  letter-spacing: 0%;
  vertical-align: middle;
  color: #fff;
  display: flex;
  align-items: center;
}

/* 下拉選單 */
.edit-select {
  width: 100%;
  padding: 8px 12px;
  border: 1.5px solid #e0e3ed;
  border-radius: 6px;
  background: #fafbff;
  color: #222;
  font-size: 15px;
  font-family: 'Noto Sans TC', sans-serif;
  appearance: none;
  transition: border 0.2s, box-shadow 0.2s;
  box-shadow: none;
  outline: none;
  cursor: pointer;
  position: relative;
}
.edit-select:focus {
  border-color: #6168FC;
  box-shadow: 0 0 0 2px #e4e7ff;
}
.edit-select:active {
  transform: scale(0.98);
}

/* 自訂下拉箭頭 */
.edit-select {
  background-image: url("data:image/svg+xml,%3Csvg width='16' height='16' fill='none' stroke='%236168FC' stroke-width='2' viewBox='0 0 24 24'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 18px 18px;
}

/* 日期、時間 input */
input[type='date'].edit-input,
input[type='time'].edit-input {
  width: 100%;
  padding: 8px 12px;
  border: 1.5px solid #e0e3ed;
  border-radius: 6px;
  background: #fafbff;
  color: #222;
  font-size: 15px;
  font-family: 'Noto Sans TC', sans-serif;
  transition: border 0.2s, box-shadow 0.2s;
  box-shadow: none;
  outline: none;
}
input[type='date'].edit-input:focus,
input[type='time'].edit-input:focus {
  border-color: #6168FC;
  box-shadow: 0 0 0 2px #e4e7ff;
}
input[type='date'].edit-input:active,
input[type='time'].edit-input:active {
  transform: scale(0.98);
}

/* 日曆、時鐘 icon 簡約化 */
input[type='date'].edit-input::-webkit-calendar-picker-indicator,
input[type='time'].edit-input::-webkit-calendar-picker-indicator {
  filter: invert(38%) sepia(98%) saturate(747%) hue-rotate(202deg) brightness(97%) contrast(92%);
  opacity: 0.7;
  transition: opacity 0.2s;
  cursor: pointer;
}
input[type='date'].edit-input:focus::-webkit-calendar-picker-indicator,
input[type='time'].edit-input:focus::-webkit-calendar-picker-indicator {
  opacity: 1;
}

.missing-field {
  color: #dc3545 !important;
  font-weight: bold;
}

.missing-field-input {
  border-color: #dc3545 !important;
  background-color: #fff5f5 !important;
}

.missing-field-input:focus {
  box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.25) !important;
}

.order-btn.update {
  background: #77B5FF !important;
  box-shadow: none;
}
.order-btn.update[disabled], .order-btn.update:disabled {
  background: #D8EAFF !important;
  box-shadow: 2px 2px 2px 0px #00000040 !important;
}

.order-btn.create {
  background: #6168FC;
  box-shadow: none;
}
.order-btn.create[disabled], .order-btn.create:disabled {
  background: #C5C7FF !important;
  box-shadow: 2px 2px 2px 0px #00000040 !important;
}
</style>