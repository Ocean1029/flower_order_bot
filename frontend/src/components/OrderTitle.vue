<template>
  <div class="order-title-wrapper">
    <div class="main-title-bar">
    <span class="main-title">{{ pageTitle }}</span>
  </div>
  </div>
  
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

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
  top: 20px;                /* 距離 .main-title-bar 上邊界 20px */
  left: 72px;
  height: 80px;
  font-family: 'Noto Sans TC', '思源黑體', 'Microsoft JhengHei', Arial, sans-serif;
  font-weight: 700;
  font-size: 32px;
  line-height: 40px;        /* 與 Figma 的 125% 相近 */
  letter-spacing: 0;
  color: #6168FC;
  background: transparent;
}
</style>
