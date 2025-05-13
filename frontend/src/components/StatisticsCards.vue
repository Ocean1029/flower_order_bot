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
  { title: '溝通中訂單',  value: props.statics.pending_orders,   icon: 'fas fa-comments',     color: '#4F8CFF' },
  { title: '本月訂單',    value: props.statics.monthly_orders,   icon: 'fas fa-list-alt',     color: '#7B61FF' },
  { title: '本月營業額',  value: `$${props.statics.monthly_income}`, icon: 'fas fa-dollar-sign', color: '#3DC9B3' }
])
</script>

<style scoped>
.stat-cards-container {
  display: flex;
  gap: 36px;
}

.stat-card {
  position: relative;
  width: 210px;
  height: 144px;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.stat-card:hover {
  background: #D8EAFF;
}

.stat-icon {
  position: absolute;
  top: 27px;
  left: 27px;
  width: 24px;
  height: 24px;
  font-size: 24px;
  color: #6168FC;
}

.stat-label {
  position: absolute;
  top: 27px;
  left: calc(27px + 24px + 8px);
  width: 156px;
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
