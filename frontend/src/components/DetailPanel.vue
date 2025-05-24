<template>
  <transition name="slide-detail">
    <div class="order-detail-panel">
      <!-- section: 最上方 bar -->
      <div class="section">
        <div class="head">
          <span class="section-title">詳細資料</span>
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
        <!-- bottom: 編輯資料按鈕 -->
        <div class="bottom">
          <div class="action-buttons">
            <div 
              class="edit" 
              :class="{ 'disabled': isEditing }"
              @click="startEditing"
            >
              <div class="icon-wrapper">
                <i class="fas fa-pen"></i>
              </div>
              <span class="button-text">編輯</span>
            </div>
            <div 
              class="save" 
              :class="{ 'active': isEditing }"
              @click="confirmEditing"
            >
              <div class="icon-wrapper">
                <i class="fas fa-check"></i>
              </div>
              <span class="button-text">確認</span>
            </div>
          </div>
        </div>
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

.section-title {
  height: 25px;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 18px;
  line-height: 140%;
  color: #000;
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

.bottom {
  position: absolute;
  left: 72px;
  bottom: 24px;
  width: 184px;
  height: 40px;
  display: flex;
  align-items: center;
  z-index: 10;
}

.action-buttons {
  display: flex;
  gap: 8px;
  width: 100%;
}

.edit, .save {
  width: 88px;
  height: 40px;
  border-radius: 12px;
  background: #6168FC;
  box-shadow: 2px 2px 2px 0px #00000040;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.edit.disabled {
  background: #C5C7FF;
  cursor: not-allowed;
}

.save {
  background: #C5C7FF;
  cursor: not-allowed;
}

.save.active {
  background: #6168FC;
  opacity: 1;
  cursor: pointer;
}

.icon-wrapper {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
}

.button-text {
  width: 32px;
  height: 18px;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 16px;
  line-height: 113%;
  letter-spacing: 0%;
  vertical-align: middle;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit i, .save i {
  color: #ffffff;
  font-size: 14px;
}
</style> 