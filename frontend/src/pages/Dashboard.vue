<template>
  <!-- 動態頁面標題，滿版對齊螢幕邊緣 -->
  <OrderTitle />
  <div class="page-content">
    <div class="dashboard-section">
      <StatisticsCards :statics="statics" />
    </div>
    <div class="dashboard-section">
      <OrderTable :data="orders" :columnName="columnName" />
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

const columnName = [
  '訂單ID', '客戶姓名', '客戶電話', '收件地址', '訂單日期', '總金額',
  '商品', '數量', '備註', '付款方式', '卡片訊息', '星期',
  '送貨日期時間', '收件人姓名', '收件人電話', '送貨地址', '訂單狀態', '送貨方式'
]

const orders = ref([])
const messages = ref([])
const statics = ref({
  today_orders: 0,
  pending_orders: 0,
  monthly_income: 0,
  total_customers: 0
})

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