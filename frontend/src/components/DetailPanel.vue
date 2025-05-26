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
          <template v-if="col === '取貨時間'">
            <!-- 第一行：標題+日期 -->
            <div class="table-row">
              <div class="table-column">{{ col }}</div>
              <div class="data-container">
                <template v-if="isEditing">
                  <input
                    type="date"
                    v-model="pickupDate"
                    class="edit-input"
                    style="width: 100%;"
                  />
                </template>
                <template v-else>
                  <span class="data">{{ pickupDateTextWithWeekday }}</span>
                </template>
              </div>
            </div>
            <!-- 第二行：空白+時間 -->
            <div class="table-row">
              <div class="table-column"></div>
              <div class="data-container">
                <template v-if="isEditing">
                  <input
                    type="time"
                    v-model="pickupTime"
                    class="edit-input"
                    style="width: 100%;"
                  />
                </template>
                <template v-else>
                  <span class="data">{{ pickupTimeText }}</span>
                </template>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="table-row">
              <div class="table-column">{{ col }}</div>
              <div class="data-container">
                <template v-if="isEditing && editableFields.includes(col)">
                  <input
                    v-model="editedData[col]"
                    class="edit-input"
                    type="text"
                  />
                </template>
                <span v-else class="data">{{ dataList[idx] }}</span>
              </div>
            </div>
          </template>
        </template>
      </div>
      <!-- bottom: frame-2 兩個新按鈕 -->
      <div class="frame-2">
          <div class="order-btn update" :class="{ editing: isEditing }">
            <i class="fas fa-upload btn-icon"></i>
            <span class="btn-text">更新工單</span>
          </div>
          <div class="order-btn create" :class="{ editing: isEditing }">
            <i class="fas fa-plus btn-icon"></i>
            <span class="btn-text">建立新工單</span>
          </div>
        </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed } from 'vue'
import { sendOrderDraft } from '@/api/orders'

const props = defineProps({
  orderData: Object,
  roomId: String
})

const emit = defineEmits(['close-detail'])

// 可編輯的欄位
const editableFields = [
  '客戶姓名', '客戶電話', '收件人姓名', '收件人電話', '品項', '數量', '備註', 
  '卡片訊息', '取貨方式', '送貨日期', '收件地址', '送貨地址', '付款方式'
]

// 依照原本順序組成資料陣列
const columns = [
  '訂單編號', '客戶姓名', '客戶電話', '收件人姓名', '收件人電話', '總金額', 
  '品項', '數量', '備註', '卡片訊息', '取貨方式', '送貨日期', '收件地址', 
  '送貨地址', '訂單日期', '訂單狀態', '付款方式', '星期'
]

const dataList = computed(() => [
  props.orderData?.id || ' ',
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
  props.orderData?.order_status || ' ',
  props.orderData?.pay_way || ' ',
  props.orderData?.weekday || ' '
])

const isEditing = ref(false)
const editedData = ref({})

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
  columns.forEach((col, idx) => {
    if (editableFields.includes(col)) {
      editedData.value[col] = dataList.value[idx]
    }
  })
}

function cancelEditing() {
  isEditing.value = false
  editedData.value = {}
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
      send_datetime: editedData.value['送貨日期'] 
        ? new Date(editedData.value['送貨日期']).toISOString().replace(/\.\d{3}Z$/, '.331Z')
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

.edit-input {
  width: 100%;
  padding: 8px;
  border: 1.5px solid #e9e9e9;
  border-radius: 4px;
  font-size: 14px;
  font-family: 'Noto Sans TC', sans-serif;
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
  background: #6168FC;
  transition: background 0.2s;
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
</style> 