<template>
  <div class="messages-container">
    <MessageItem
      v-for="message in processedMessages"
      :key="message.id"
      :message="message"
    />
  </div>
</template>
<script setup>
import MessageItem from './MessageItem.vue'
import { computed } from 'vue'

const props = defineProps({
  messages: Array
})

// 自動標記 isFirstInMinute
const processedMessages = computed(() => {
  const result = []
  let lastDate = null
  props.messages.forEach((msg, idx, arr) => {
    // 取得訊息日期字串
    const msgDate = new Date(msg.timestamp)
    const dateStr = `${msgDate.getMonth() + 1}/${msgDate.getDate()}（${'日一二三四五六'[msgDate.getDay()]}）`
    if (!lastDate || lastDate !== dateStr) {
      // 插入日期訊息
      result.push({
        id: `date-${dateStr}-${idx}`,
        isDate: true,
        text: dateStr
      })
      lastDate = dateStr
    }
    // 判斷 isFirstInMinute
    let isFirstInMinute = false
    if (msg.direction === 'incoming') {
      if (idx === 0) isFirstInMinute = true
      else {
        const prev = arr[idx - 1]
        isFirstInMinute = prev.direction !== 'incoming' ||
          (new Date(msg.timestamp).getMinutes() !== new Date(prev.timestamp).getMinutes())
      }
    }
    result.push({ ...msg, isFirstInMinute })
  })
  return result
})
</script>
<style scoped>

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  box-sizing: border-box;
  background: #f5f6fa;
}
.messages-container {
  flex: 1;
  height: 90%;
  overflow-y: auto;
  padding: 24px 24px;
  box-sizing: border-box;
  background: #FFFFFF;
}
.message-bubble,
.sender {
  max-width: 360px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.input-container {
  position: fixed;
  left: 50%;
  bottom: 40px; 
  transform: translateX(-50%);
  width: 60%;
  max-width: 600px;
  min-width: 300px;
  z-index: 100;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 24px;
  padding: 12px 24px;
  display: flex;
  align-items: center;
}

.chat-room-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 56px);  /* 扣除上方 navbar */
  overflow: hidden;             /* 禁止最外層捲動 */
}

</style> 