<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  statics: {
    type: Object,
    required: true
  }
})

const activeIndex = ref(1) // 預設選中第二個卡片（溝通中訂單）

const statList = computed(() => [
  { title: '今日訂單', value: props.statics.today_orders, icon: 'fa-regular fa-calendar', color: '#007AFF' },
  { title: '溝通中訂單', value: props.statics.pending_orders, icon: 'fa-regular fa-comments', color: '#4F8CFF' },
  { title: '本月訂單', value: props.statics.monthly_orders, icon: 'fa-regular fa-list-alt', color: '#7B61FF' }, // 假資料
  { title: '本月營業額', value: `$${props.statics.monthly_income}`, icon: 'fa-solid fa-dollar-sign', color: '#3DC9B3' } // 假資料
  
])
</script>

<template>
  <div class="stat-cards-row">
    <div
      v-for="(card, idx) in statList"
      :key="card.title"
      class="stat-card"
      :class="{ active: idx === activeIndex }"
      :style="{ borderColor: card.color }"
      @click="activeIndex = idx"
    >
      <div class="icon-circle" :style="{ background: card.color }">
        <i :class="card.icon"></i>
      </div>
      <div class="stat-title">{{ card.title }}</div>
      <div class="stat-value">{{ card.value }}</div>
    </div>
  </div>
</template>

<style scoped>
.stat-cards-row {
  display: flex;
  gap: 32px;
  margin: 32px 0 24px 0;
  justify-content: flex-start;
}
.stat-card {
  flex: 1;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(79,140,255,0.10);
  padding: 28px 0 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 2px solid transparent;
  cursor: pointer;
  transition: box-shadow 0.2s, border-color 0.2s, background 0.2s;
  min-width: 180px;
}
.stat-card.active {
  background: var(--gray-100);
  border-color: var(--primary);
  box-shadow: 0 8px 24px rgba(79,140,255,0.12);
}
.icon-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.7rem;
  margin-bottom: 14px;
}
.stat-title {
  font-size: 16px;
  color: var(--primary-dark);
  margin-bottom: 8px;
  font-weight: 700;
  letter-spacing: 1px;
}
.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: var(--primary-dark);
  letter-spacing: 1px;
  margin-top: 2px;
}
</style>
  
