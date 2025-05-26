<template>
  <div class="stat-cards-container">
    <div
      v-for="card in statList"
      :key="card.title"
      class="stat-card"
    >
      <i :class="card.icon" class="stat-icon" />
      <span class="stat-label">{{ card.title }}</span>
      <span class="stat-number">{{ card.value }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  statics: {
    type: Object,
    required: true
  }
})

const statList = computed(() => [
  { title: '今日訂單',    value: props.statics.today_orders,     icon: 'fas fa-calendar',     color: '#007AFF' },
  { title: '待處理訂單',  value: props.statics.pending_orders,   icon: 'fas fa-comment',     color: '#4F8CFF' },
  { title: '本月營業額',  value: `$${props.statics.monthly_income}`, icon: 'fas fa-dollar-sign', color: '#3DC9B3' },
  { title: '顧客總數',    value: props.statics.total_customers,   icon: 'fas fa-users',        color: '#FFB347' }
])
</script>

<style scoped>
.stat-cards-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0px;
  gap: 36px;
  width: 948px;
  height: 144px;
  margin-left: 64px;
  background: transparent;
}

.stat-card {
  position: relative;
  width: 210px;
  height: 144px;
  background: #fff;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.25);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  flex: none;
  order: 0;
  flex-grow: 1;
}
.stat-card:hover {
  background: #D8EAFF;
}

.stat-icon {
  position: absolute;
  top: 27px;
  left: 38px;
  width: 24px;
  height: 24px;
  font-size: 24px;
  color: #6168FC;
  padding: 8 8;
  gap: 8;
}

.stat-label {
  position: absolute;
  top: 25px;
  left: calc(27px + 24px + 20px);
  height: 28px;
  display: flex;
  align-items: center;
  font-family: 'Noto Sans TC', '思源黑體', 'Microsoft JhengHei', Arial, sans-serif;
  font-weight: 700;
  font-size: 16px;
  line-height: 28px;
  letter-spacing: 0;
  color: #6168FC;
  padding: 0 8px;
}

.stat-number {
  position: absolute;
  top: 69px;
  left: 81px;
  width: 48px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Noto Sans TC', '思源黑體', 'Microsoft JhengHei', Arial, sans-serif;
  font-weight: 700;
  font-size: 40px;
  line-height: 50px;
  text-align: center;
  letter-spacing: 0;
  color: #6168FC;
}
</style>
