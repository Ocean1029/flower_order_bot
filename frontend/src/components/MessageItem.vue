<template>
  <!-- 日期區塊 -->
  <div v-if="message.isDate" class="date-block">
    <span class="date-text">{{ message.text }}</span>
  </div>

  <!-- 對方訊息（message customer） -->
  <div v-else-if="message.direction === 'incoming'" class="message-customer">
    <img
      v-if="message.isFirstInMinute"
      class="pic"
      :src="message.avatar || ''"
      :alt="message.sender"
      @error="onImgError"
    />
    <div class="message-bubble">
      <div class="sender">
        <span class="message-text">{{ message.text }}</span>
      </div>
      <span class="time">{{ formatTime(message.timestamp) }}</span>
    </div>
  </div>

  <!-- 自己訊息（message myself） -->
  <div v-else class="message-myself">
    <div class="message-bubble">
      <div class="sender myself">
        <span class="message-text">{{ message.text }}</span>
      </div>
      <span class="time myself">{{ formatTime(message.timestamp) }}</span>
    </div>
  </div>
</template>

<script setup>
import { format } from 'date-fns'
import { computed } from 'vue'

const props = defineProps({
  message: Object
})

const isOutgoing = computed(() => {
  return props.message.direction === 'outgoing_by_staff' || 
         props.message.direction === 'outgoing_by_bot'
})

function formatTime(timestamp) {
  return format(new Date(timestamp), 'HH:mm')
}
function onImgError(event) {
  event.target.src = '' // 讓 src 變空，觸發預設灰色圈圈樣式
}
</script>

<style scoped>
/* 日期區塊 */
.date-block {
  width: 87px;
  height: 24px;
  margin: 0 auto 12px;
  border-radius: 8px;
  padding: 2px 8px;
  background: #C5C7FF;
  display: flex;
  align-items: center;
  justify-content: center;
}
.date-text {
  font-family: 'Noto Sans TC';
  font-weight: 400;
  font-size: 14px;
  line-height: 140%;
  color: #fff;
  text-align: center;
}

.message-bubble {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  min-height: 40px;
  max-width: 360px;
}

/* 對方訊息 */
.message-customer {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  min-height: 40px;
  margin-left: 0;
  margin-bottom: 12px;
}
.pic {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 4px;
  background: #D9D9D9;
  /* 沒有 src 時顯示灰色 */
  display: inline-block;
}
.pic[src=""] {
  background: #D9D9D9;
}

.sender {
  min-height: 40px;
  max-width: 360px;
  border-radius: 24px;
  padding: 9px 16px;
  background: #F2F2F2;
  word-break: break-word;
  
  display: inline-block;
  align-items: center;
}
.message-text {
  font-family: 'Noto Sans TC';
  font-weight: 400;
  font-size: 16px;
  line-height: 140%;
  color: #000000DE;
}
.time {
  width: 50px;
  height: 17px;
  font-family: 'Noto Sans TC';
  font-weight: 400;
  font-size: 12px;
  line-height: 140%;
  color: #00000061;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0px;
}

/* 自己訊息 */
.message-myself {
  display: flex;
  justify-content: flex-end;
  min-height: 40px;
  margin-right: 0;
  margin-bottom: 12px;
}
.message-myself .message-bubble {
  flex-direction: row-reverse;
  gap: 2px;
}
.sender.myself {
  background: #77B5FF;
  color: #fff;
}
.message-myself .message-text {
  color: #fff;
}
.time.myself {
  width: 44px;
  color: #00000061;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 4px;
  margin-left: 0;
  padding: 0 6px;
}
</style> 