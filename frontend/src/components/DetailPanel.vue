<template>
  <div class="detail-panel">
    <button class="close-btn" @click="$emit('close')">
      <i class="fas fa-angle-double-right"></i>
    </button>
    <h3 class="panel-title">詳細資料</h3>
    <div class="detail-row" v-if="room">
      <div class="detail-label">訂單編號</div>
      <div class="detail-value">{{ room.orderId || '-' }}</div>
    </div>
    <div class="detail-row">
      <div class="detail-label">姓名</div>
      <div class="detail-value">{{ room.name || '-' }}</div>
    </div>
    <div class="detail-row">
      <div class="detail-label">電話</div>
      <div class="detail-value">{{ room.phone || '-' }}</div>
    </div>
    <div class="detail-row">
      <div class="detail-label">品項</div>
      <div class="detail-value">{{ room.product || '-' }}</div>
    </div>
    <div class="detail-row">
      <div class="detail-label">數量</div>
      <div class="detail-value">{{ room.qty || '-' }}</div>
    </div>
    <div class="detail-row">
      <div class="detail-label">備註</div>
      <div class="detail-value">{{ room.note || '-' }}</div>
    </div>
    <div class="detail-row">
      <div class="detail-label">取貨方式</div>
      <div class="detail-value">{{ room.pickupMethod || '-' }}</div>
    </div>
    <div class="detail-row">
      <div class="detail-label">取貨時間</div>
      <div class="detail-value">{{ room.pickupTime || '-' }}</div>
    </div>
    <div class="detail-row">
      <div class="detail-label">金額</div>
      <div class="detail-value">{{ room.amount ? 'NT ' + room.amount : '-' }}</div>
    </div>
    <div class="detail-row">
      <div class="detail-label">付款方式</div>
      <div class="detail-value">{{ room.paymentMethod || '-' }}</div>
    </div>
    <div class="detail-row">
      <div class="detail-label">付款狀態</div>
      <div class="detail-value">{{ room.paymentStatus || '-' }}</div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  room: Object
})
</script>

<style scoped>
.detail-panel {
  width: 100%;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(79,140,255,0.06);
  padding: 18px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: relative;
}
.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: none;
  border: none;
  font-size: 22px;
  color: #6168FC;
  cursor: pointer;
  z-index: 10;
}
.close-btn:hover {
  color: #FF6F91;
}
.panel-title {
  font-size: 20px;
  font-weight: 700;
  color: #6168FC;
  margin-bottom: 18px;
}
.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid #f0f0f0;
}
.detail-label {
  color: #888;
  font-size: 15px;
  width: 110px;
}
.detail-value {
  color: #333;
  font-size: 15px;
  font-weight: 500;
  text-align: right;
  flex: 1;
}
</style> 