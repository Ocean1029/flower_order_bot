<script setup>
import OrderTable from '@/components/OrderTable.vue'
import { ref, onMounted } from 'vue'
import { fetchOrders} from '@/api/orders'

const columnName = [
  '匯出工單', '訂單編號', '狀態', '取貨時間', '姓名', '電話', '商品', '數量',
  '備註', '取貨方式', '金額', '付款方式', '付款狀態', '取消訂單'
]

const orders = ref([])
const isLoading = ref(true)
const error = ref(null)
const currentDate = ref(new Date())

const formatDate = (date) => {
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

const goToPreviousDay = () => {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() - 1)
  currentDate.value = newDate
  // TODO: Add logic to fetch orders for the new date
}

const goToNextDay = () => {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() + 1)
  currentDate.value = newDate
  // TODO: Add logic to fetch orders for the new date
}

onMounted(async () => {
  isLoading.value = true
  error.value = null
  
  try {
    orders.value = await fetchOrders()
  } catch (err) {
    console.error('Error fetching orders:', err)
    error.value = '無法載入訂單資料，請稍後再試'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="order-title-wrapper">
    <div class="main-title-bar">
      <span class="main-title">訂單管理</span>
    </div>
  </div>
  <div class="page-content">
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else-if="isLoading" class="loading-message">
      載入中...
    </div>
    <OrderTable v-else :data="orders" :columnName="columnName" />
  </div>
</template>

<style scoped>
.order-title-wrapper {
  position: absolute;
  top: 56px;
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
  height: 40px;
  font-family: 'Noto Sans TC', '思源黑體', 'Microsoft JhengHei', Arial, sans-serif;
  font-weight: 700;
  font-size: 32px;
  line-height: 40px;
  letter-spacing: 0;
  color: #6168FC;
  background: transparent;
}

.page-content {
  padding-top: 160px;
  padding-left: 8px;
  padding-right: 8px;
  max-width: 1280px;
  margin: 0 auto;
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
</style>