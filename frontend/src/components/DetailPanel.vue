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
        <div
          class="table-row"
          v-for="(col, idx) in columns"
          :key="col"
        >
          <div class="table-column">{{ col }}</div>
          <div class="data-container">
            <input 
              v-if="isEditing && editableFields.includes(col)"
              v-model="editedData[col]"
              class="edit-input"
              type="text"
            />
            <span v-else class="data">{{ dataList[idx] }}</span>
          </div>
        </div>
        
      </div>
      <!-- bottom: 兩個新按鈕 -->
      <div class="bottom-btns">
          <button class="order-btn update">更新工單</button>
          <button class="order-btn create">建立新工單</button>
        </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const props = defineProps({
  room: Object
})

const emit = defineEmits(['close-detail'])

// 可編輯的欄位
const editableFields = [
  '姓名', '品項', '電話', '數量', '備註', '取貨方式', '取貨時間', '金額', '付款方式', '付款狀態'
]

// 依照原本順序組成資料陣列
const columns = [
  '訂單編號', '姓名', '品項','電話', '數量', '備註', '取貨方式', '取貨時間', '金額', '付款方式', '付款狀態'
]

const dataList = [
  props.room?.orderId || ' ',
  props.room?.name || ' ',
  props.room?.product || ' ',
  props.room?.qty || ' ',
  props.room?.note || ' ',
  props.room?.pickupMethod || ' ',
  props.room?.pickupTime || ' ',
  props.room?.amount ? 'NT ' + props.room.amount : ' ',
  props.room?.paymentMethod || ' ',
  props.room?.paymentStatus || ' '
]

const isEditing = ref(false)
const editedData = ref({})

function startEditing() {
  isEditing.value = true
  // 初始化編輯數據
  columns.forEach((col, idx) => {
    if (editableFields.includes(col)) {
      editedData.value[col] = dataList[idx]
    }
  })
}

function cancelEditing() {
  isEditing.value = false
  editedData.value = {}
}

function confirmEditing() {
  // 這裡可以添加保存邏輯
  isEditing.value = false
  // 更新數據
  columns.forEach((col, idx) => {
    if (editableFields.includes(col)) {
      dataList[idx] = editedData.value[col]
    }
  })
  editedData.value = {}
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

.bottom-btns {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 32px;
}

.order-btn {
  min-width: 100px;
  height: 40px;
  border-radius: 12px;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 16px;
  border: none;
  cursor: pointer;
  box-shadow: 2px 2px 2px 0px #00000020;
  transition: background 0.2s;
}

.order-btn.update {
  background: #C5C7FF;
  color: #6168FC;
}

.order-btn.create {
  background: #6168FC;
  color: #fff;
}
</style> 