<script setup>
import OrderTable from '@/components/OrderTable.vue'
import ConversationList from '@/components/ConversationList.vue'
import StatisticsCards from '@/components/StatisticsCards.vue'
import { onMounted, ref } from 'vue'
import {  fetchOrders } from '@/api/orders'
import { fetchStaticData } from '@/api/statics'
import { getLatestMessages } from '@/api/messages'
import { mockOrders, mockStats, mockMessages } from '@/mockData.js'

const columnName = [
  '訂單ID', '姓名', '電話', '花材', '數量', '預算',
  '取貨方式', '取貨日期', '取貨時間', '付款狀態', '已付款金額', '備註'
]

const orders = ref([])
const messages = ref([])
const statics = ref([])

onMounted(async () => {
  try {
    orders.value = await fetchOrders()
  } catch (err) {
    console.error('無法取得訂單資料', err)
  }
  try {
    messages.value = await getLatestMessages()
  } catch (err) {
    console.error('無法取得訊息資料', err)
  }
  try {
    statics.value = await fetchStaticData()
  } catch (err) {
    console.error('無法取得統計資料', err)
  }
})
</script>

<template>
  <StatisticsCards :statics="mockStats" />
  <OrderTable :data="mockOrders" :columnName="columnName" />
  <ConversationList :messages="mockMessages" />
</template>
