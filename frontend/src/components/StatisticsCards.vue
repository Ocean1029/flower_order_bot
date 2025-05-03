<script setup>
import { computed } from 'vue'
const props = defineProps({
  statics: {
    type: Object,
    required: true
  }
})

const statList = computed(() => [
  { title: '今日訂單', value: props.statics.today_orders },
  { title: '待處理', value: props.statics.pending_orders },
  { title: '本月收入', value: `$${props.statics.monthly_income}` },
  { title: '顧客數', value: props.statics.total_customers }
])
</script>


<template>
    <div id="statistics" class="section mt-4">
      <div class="header">
        <h2><i class="fas fa-chart-bar me-2"></i>數據統計</h2>
      </div>
      <div class="row">
        <div class="col-md-3" v-for="card in statList" :key="card.title">
          <div class="stat-card">
            <h3>{{ card.title }}</h3>
            <p class="stat-number">{{ card.value }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
