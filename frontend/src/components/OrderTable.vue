<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  columnName: {
    type: Array,
    required: true
  }
})

const searchText = ref('')

// 篩選符合搜尋文字的訂單
const filteredData = computed(() => {
  return Array.isArray(props.data)
    ? props.data.filter(row =>
        Object.values(row || {}).some(value =>
          String(value).toLowerCase().includes(searchText.value.toLowerCase())
        )
      )
    : []
})

// 匯出成 CSV 檔案
function downloadCSV() {
  const headers = props.columnName
  const rows = props.data.map(row => [
    row.id,
    row.customer_name,
    row.phone,
    row.flower,
    row.qty,
    row.budget,
    row.pickup_method,
    row.pickup_date,
    row.pickup_time,
    row.note
  ])

  const csvContent = [headers, ...rows]
    .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
    .join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', '訂單資料.csv')
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<template>
  <div class="section" id="orders">
    <div class="header d-flex justify-content-between align-items-center">
      <h2><i class="fas fa-shopping-bag me-2"></i>花店訂單總覽</h2>
      <button @click="downloadCSV" class="download-btn">
        <i class="fas fa-download"></i> 下載 CSV
      </button>
    </div>

    <div class="search-container">
      <div class="input-group">
        <span class="input-group-text bg-white border-end-0">
          <i class="fas fa-search text-primary"></i>
        </span>
        <input
          type="text"
          v-model="searchText"
          class="form-control search-input border-start-0"
          placeholder="搜尋訂單（姓名、電話、花材等）"
        />
      </div>
    </div>

    <div class="table-container table-responsive">
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th v-for="col in props.columnName" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in filteredData" :key="row.id">
            <td>{{ row.id }}</td>
            <td>{{ row.customer_name }}</td>
            <td>{{ row.phone }}</td>
            <td>{{ row.flower }}</td>
            <td>{{ row.qty }}</td>
            <td>{{ row.budget }}</td>
            <td>{{ row.pickup_method }}</td>
            <td>{{ row.pickup_date }}</td>
            <td>{{ row.pickup_time }}</td>
            <td>{{ row.note }}</td>
          </tr>
        </tbody>
      </table>

      <div v-if="filteredData.length === 0" class="no-results">
        <i class="fas fa-search fa-2x mb-3"></i>
        <p>找不到符合條件的訂單</p>
      </div>
    </div>
  </div>
</template>
