<script setup>
import OrderTable from '@/components/OrderTable.vue'
import { ref, onMounted } from 'vue'
import { fetchOrders} from '@/api/orders'

const columnName = [
  '訂單ID', '客戶姓名', '客戶電話', '收件地址', '訂單日期', '總金額',
  '商品', '數量', '備註', '付款方式', '卡片訊息', '星期',
  '送貨日期時間', '收件人姓名', '收件人電話', '送貨地址', '訂單狀態', '送貨方式'
]

const orders = ref([])
const isLoading = ref(true)
const error = ref(null)

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