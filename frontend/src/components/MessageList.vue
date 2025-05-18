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
    if (!msg.isSelf) {
      if (idx === 0) isFirstInMinute = true
      else {
        const prev = arr[idx - 1]
        isFirstInMinute = prev.isSelf ||
          (new Date(msg.timestamp).getMinutes() !== new Date(prev.timestamp).getMinutes())
      }
    }
    result.push({ ...msg, isFirstInMinute })
  })
  return result
})
</script>
<style scoped>
.messages-container {
  width: 664px;
  height: 100%;
  left: 440px;
  flex: 1;
  overflow-y: auto;
  padding: 24px 0;   /* 上下 24px，左右 0，讓訊息靠近左右邊 */
  max-width: 619px;  /* 跟設計稿一致 */
  margin: 0 auto;    /* 置中 */
  width: 100%;
}
</style> 