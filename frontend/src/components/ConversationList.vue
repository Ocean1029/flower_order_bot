<template>
    <div id="conversations" class="section mt-4">
      <div class="header d-flex justify-content-between align-items-center">
        <h2><i class="fas fa-comments me-2"></i>對話記錄</h2>
        <div class="filter-container">
          <select v-model="filter" class="form-select me-2" style="width: 150px;">
            <option value="all">全部顧客</option>
            <option value="today">今日對話</option>
            <option value="week">本週對話</option>
          </select>
        </div>
      </div>
  
      <div class="conversation-list">
        <div v-for="message in filteredMessages" :key="message.id" class="conversation-item">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <div>
              <h5 class="mb-0">{{ message.customer_name || '未知顧客' }}</h5>
              <small class="text-muted">{{ message.phone || '' }}</small>
            </div>
          </div>
          <div class="conversation-preview">
            <p class="mb-0">{{ message.preview }}</p>
            <small class="text-muted">{{ message.time }}</small>
          </div>
          <button class="btn btn-link p-0 mt-2" :data-conversation-id="message.id">查看完整對話</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { isToday, isThisWeek, parseISO } from 'date-fns'
  
  const props = defineProps({
    messages: Array
  })
  
  const filter = ref('all')
  
  const filteredMessages = computed(() => {
    if (filter.value === 'today') {
      return props.messages.filter(m => isToday(parseISO(m.time)))
    } else if (filter.value === 'week') {
      return props.messages.filter(m => isThisWeek(parseISO(m.time)))
    }
    return props.messages
  })
  </script>
  