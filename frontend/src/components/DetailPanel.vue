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
          :class="{ 'with-border': idx === 5 }"
          v-for="(col, idx) in columns"
          :key="col"
        >
          <div class="table-column">{{ col }}</div>
          <span class="data">{{ dataList[idx] }}</span>
        </div>
        <!-- bottom: 編輯資料按鈕 -->
        <div class="bottom">
          <i class="fas fa-pen edit-icon"></i>
          <span class="edit-text">編輯資料</span>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { defineEmits } from 'vue'

const props = defineProps({
  room: Object
})

const emit = defineEmits(['close-detail'])

// 依照原本順序組成資料陣列
const columns = [
  '訂單編號', '姓名', '品項','電話', '數量', '備註', '取貨方式', '取貨時間', '金額', '付款方式', '付款狀態'
]
const dataList = [
  props.room?.orderId || '-',
  props.room?.name || '-',
  props.room?.product || '-',
  props.room?.qty || '-',
  props.room?.note || '-',
  props.room?.pickupMethod || '-',
  props.room?.pickupTime || '-',
  props.room?.amount ? 'NT ' + props.room.amount : '-',
  props.room?.paymentMethod || '-',
  props.room?.paymentStatus || '-'
]
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
.table-row.with-border {
  border: 0.5px solid #B3B3B3;
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
.data {
  flex: 1;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 16px;
  line-height: 140%;
  color: #000;
  background: none;
  vertical-align: middle;
}
.bottom {
  position: absolute;
  left: 50%;
  bottom: 24px;
  transform: translateX(-50%);
  width: 119px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: 12px;
  padding: 8px 8px;
  background: #6168FC;
  box-shadow: 2px 2px 2px 0px #00000040;
  cursor: pointer;
  z-index: 10;
}
.edit-icon {
  right: 3px;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.edit-text {
  height: 18px;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 15px;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 18px;
}
</style> 