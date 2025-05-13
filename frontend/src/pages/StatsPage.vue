<script setup>
import StatisticsCards from '@/components/StatisticsCards.vue'
import { onMounted, ref } from 'vue'
import { fetchStaticData } from '@/api/statics'

const statics = ref([])

onMounted(async () => {
  try {
    statics.value = await fetchStaticData()
  } catch (err) {
    console.error('無法取得訊息資料', err)
  }
})
</script>

<template>
  <div class="page-content">
    <StatisticsCards :statics="statics" />
  </div>
</template>
