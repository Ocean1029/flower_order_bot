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
import { ref, defineEmits, watch, computed } from 'vue'

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

// 新增：取貨時間的日期與時間欄位
const pickupDate = ref('')
const pickupTime = ref('')

const pickupDateText = computed(() => {
  // 取貨時間格式：'YYYY-MM-DDTHH:mm:ss'
  const val = dataList[columns.indexOf('取貨時間')]
  if (!val || !val.includes('T')) return ''
  return val.split('T')[0]
})
const pickupDateTextWithWeekday = computed(() => {
  const dateStr = pickupDateText.value
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  return `${dateStr}（${weekdays[date.getDay()]}）`
})
const pickupTimeText = computed(() => {
  const val = dataList[columns.indexOf('取貨時間')]
  if (!val || !val.includes('T')) return ''
  return val.split('T')[1]?.slice(0,5) || ''
})

watch(isEditing, (val) => {
  if (val) {
    // 進入編輯時，將取貨時間拆成日期與時間
    const pickup = editedData.value['取貨時間'] || ''
    if (pickup && pickup.includes('T')) {
      pickupDate.value = pickup.split('T')[0]
      pickupTime.value = pickup.split('T')[1]?.slice(0,5) || ''
    } else {
      pickupDate.value = ''
      pickupTime.value = ''
    }
  }
})

function startEditing() {
  isEditing.value = true
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
  // 如果有取貨時間，組合成標準格式
  if (pickupDate.value && pickupTime.value) {
    editedData.value['取貨時間'] = `${pickupDate.value}T${pickupTime.value}:00`
  }
  isEditing.value = false
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