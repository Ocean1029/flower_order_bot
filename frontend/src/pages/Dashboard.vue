<template>
  <!-- 動態頁面標題，滿版對齊螢幕邊緣 -->
  <OrderTitle />
  <div class="page-content">
    <div class="dashboard-section">
      <StatisticsCards :statics="mockStats" />
    </div>
    <div class="dashboard-section">
      <OrderTable :data="orders" :columnName="columnName" />
    </div>
    <div class="dashboard-section">
      <ConversationList :messages="messages" />
    </div>
  </div>
</template>

<script setup>
import OrderTitle from '@/components/OrderTitle.vue'
import StatisticsCards from '@/components/StatisticsCards.vue'
import OrderTable from '@/components/OrderTable.vue'
import ConversationList from '@/components/ConversationList.vue'
import { onMounted, ref } from 'vue'
import { fetchOrders } from '@/api/orders'
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

<style>
.page-content {
  padding-top: 160px; /* 80px (navbar) + 80px (ordertitle) */
  padding-left: 8px;
  padding-right: 8px;
  max-width: 1280px;
  margin: 0 auto;
}
.dashboard-section + .dashboard-section {
  margin-top: 32px;
}
</style>