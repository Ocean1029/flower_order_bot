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

onMounted(async () => {
  orders.value = await fetchOrders()
})
</script>

<template>
  <div class="page-content">
    <OrderTable :data="orders" :columnName="columnName" />
  </div>
</template>