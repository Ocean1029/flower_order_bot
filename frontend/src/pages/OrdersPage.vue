<script setup>
import OrderTable from '@/components/OrderTable.vue'
import { ref, onMounted } from 'vue'
import { fetchOrders} from '@/api/orders'

const columnName = [
  '訂單ID', '姓名', '電話', '花材', '數量', '預算',
  '取貨方式', '取貨日期', '取貨時間', '付款狀態', '已付款金額', '備註'
]

const orders = ref([])

onMounted(async () => {
  orders.value = await fetchOrders()
})
</script>

<template>
  <OrderTable :data="orders" :columnName="columnName" />
</template>