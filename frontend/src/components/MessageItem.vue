<template>
  <div :class="['message', message.isSelf ? 'self' : 'other']">
    <div class="message-content">
      <div class="message-sender">{{ message.sender }}</div>
      <div class="message-text">{{ message.text }}</div>
      <div class="message-time">{{ formatTime(message.timestamp) }}</div>
    </div>
  </div>
</template>
<script setup>
import { format } from 'date-fns'
const props = defineProps({
  message: Object
})
function formatTime(timestamp) {
  return format(new Date(timestamp), 'HH:mm')
}
</script>
<style scoped>
.message {
  margin-bottom: 1rem;
  display: flex;
}
.message.self {
  justify-content: flex-end;
}
.message-content {
  max-width: 70%;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.message.self .message-content {
  background-color: #007AFF;
  color: white;
}
.message-sender {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.25rem;
}
.message.self .message-sender {
  color: #fff;
}
.message-time {
  font-size: 0.7rem;
  color: #999;
  margin-top: 0.25rem;
}
.message.self .message-time {
  color: rgba(255,255,255,0.8);
}
</style> 