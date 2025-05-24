<template>
  <!-- 動態頁面標題，滿版對齊螢幕邊緣 -->
  <div class="order-title-wrapper">
    <div class="main-title-bar">
      <span class="main-title">訂單管理平台</span>
    </div>
  </div>
  <div class="page-content">
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else>
      <div class="dashboard-section">
        <StatisticsCards :statics="statics" />
      </div>
      <div class="dashboard-section">
        <div v-if="isLoading" class="loading-message">
          載入中...
        </div>
        <OrderTable v-else :data="orders" :columnName="columnName" />
      </div>
    </div>
  </div>
</template>

<script setup>
import StatisticsCards from '@/components/StatisticsCards.vue'
import OrderTable from '@/components/OrderTable.vue'
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
const isLoading = ref(true)
const error = ref(null)

onMounted(async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const [ordersData, messagesData, statsData] = await Promise.all([
      fetchOrders(),
      getLatestMessages(),
      fetchStaticData()
    ])
    
    orders.value = ordersData
    messages.value = messagesData
    statics.value = statsData
  } catch (err) {
    console.error('Error fetching data:', err)
    error.value = '無法載入資料，請稍後再試'
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.order-title-wrapper {
  position: absolute;
  top: 80px;
  left: 0;
  width: 100vw;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  z-index: 0;
}

.main-title-bar {
  position: relative;
  width: 100vw;
  height: 80px;
  border-bottom: 1px solid #00000061
}

.main-title {
  position: relative;
  top: 20px;
  left: 72px;
  height: 80px;
  font-family: 'Noto Sans TC', '思源黑體', 'Microsoft JhengHei', Arial, sans-serif;
  font-weight: 700;
  font-size: 32px;
  line-height: 40px;
  letter-spacing: 0;
  color: #6168FC;
  background: transpare
}
.order-title-wrapper {
  position: absolute;
  top: 80px;
  left: 0;
  width: 100vw;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  z-index: 0;
}

.main-title-bar {
  position: relative;
  width: 100vw;
  height: 80px;
  border-bottom: 1px solid #00000061
}

.main-title {
  position: relative;
  top: 20px;
  left: 72px;
  height: 80px;
  font-family: 'Noto Sans TC', '思源黑體', 'Microsoft JhengHei', Arial, sans-serif;
  font-weight: 700;
  font-size: 32px;
  line-height: 40px;
  letter-spacing: 0;
  color: #6168FC;
  background: transparent;
}
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
.error-message {
  color: #dc3545;
  text-align: center;
  padding: 20px;
  font-size: 18px;
  font-weight: 500;
}
.loading-message {
  text-align: center;
  padding: 20px;
  font-size: 18px;
  color: #6168FC;
}

.dashboard-section {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 32px;
  border-bottom: 1.5px solid #e9e9e9;
}
</style>