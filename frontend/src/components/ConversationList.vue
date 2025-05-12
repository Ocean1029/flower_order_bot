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
  
  <style scoped>
  .section {
    padding: 28px 32px 20px 32px;
    background: #fff;
    border-radius: 20px;
    box-shadow: 0 4px 24px rgba(79,140,255,0.10);
    margin-top: 32px;
  }
  .header {
    margin-bottom: 18px;
  }
  .filter-container select {
    border-radius: 8px;
    border: 1.5px solid #eaf2ff;
    background: #f5f6fa;
    color: var(--primary-dark);
    font-size: 15px;
    padding: 6px 12px;
  }
  .conversation-list {
    display: flex;
    flex-direction: column;
    gap: 18px;
  }
  .conversation-item {
    background: #f5f6fa;
    border-radius: 14px;
    padding: 18px 20px 14px 20px;
    box-shadow: 0 2px 8px rgba(79,140,255,0.06);
    display: flex;
    flex-direction: column;
    transition: box-shadow 0.2s, background 0.2s;
  }
  .conversation-item:hover {
    background: #eaf2ff;
    box-shadow: 0 4px 16px rgba(79,140,255,0.10);
  }
  .conversation-preview {
    color: var(--text-sub);
    font-size: 15px;
    margin-bottom: 2px;
  }
  .conversation-item h5 {
    font-size: 16px;
    font-weight: 700;
    color: var(--primary-dark);
    margin-bottom: 2px;
  }
  .conversation-item small {
    color: var(--text-light);
    font-size: 13px;
  }
  .btn-link {
    color: var(--primary);
    font-size: 14px;
    font-weight: 700;
    text-decoration: underline;
    margin-top: 4px;
  }
  </style>
  