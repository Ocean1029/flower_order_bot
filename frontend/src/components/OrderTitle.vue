<template>
  <div class="order-title-wrapper">
    <div class="main-title-bar">
      <span
        class="main-title"
        :class="{ 'message-title': isMessagePage }"
      >
        <template v-if="isMessagePage">
          <i class="fas fa-comment-dots message-icon"></i>
          <span class="message-text">Message</span>
          <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
        </template>
        <template v-else>
          {{ pageTitle }}
        </template>
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  unreadCount: {
    type: Number,
    default: 0
  }
})

const route = useRoute()

const isMessagePage = computed(() => route.path === '/messages')

const pageTitle = computed(() => {
  if (route.path === '/') return '訂單管理平台'
  if (route.path === '/orders') return '訂單管理'
  if (route.path === '/stats') return '統計數據'
  if (route.path === '/messages') return 'Message'
  if (route.name === 'chat-room') {
    return route.state?.roomName || '聊天室'
  }
  return '訂單管理平台'
})
</script>

<style scoped>
.order-title-wrapper {
  position: relative;
  top: 80px;
  width: 100vw;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  z-index: 100;
}

.main-title-bar {
  position: relative;
  width: 100vw;
  height: 80px;
  border-bottom: 1px solid #00000061;
  background: #fff;
  display: flex;
  align-items: center;
}

.main-title {
  position: relative;
  top: 0;
  left: 72px;
  height: 64px;
  display: flex;
  align-items: center;
  font-family: 'Noto Sans TC', '思源黑體', 'Microsoft JhengHei', Arial, sans-serif;
  font-weight: 700;
  font-size: 28px;
  line-height: 40px;
  letter-spacing: 0;
  color: #6168FC;
  background: transparent;
  gap: 16px;
}
.message-title {
  left: 24px !important;
  gap: 12px;
}
.message-icon {
  font-size: 26px;
  color: #4F8CFF;
  margin-right: 10px;
  margin-left: 0;
}
.message-title .message-icon {
  margin-left: 0;
}
.message-text {
  display: inline-block;
}
.unread-badge {
  display: inline-block;
  background: #FF6F91;
  color: #fff;
  font-size: 16px;
  font-weight: 700;
  border-radius: 16px;
  padding: 2px 10px;
  margin-left: 8px;
  min-width: 28px;
  text-align: center;
}
</style>
