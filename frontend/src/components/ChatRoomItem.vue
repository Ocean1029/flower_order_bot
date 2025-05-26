<template>
  <div class="chat-room-item" @click="$emit('click')">
    <img class="avatar" :src="room.avatar" alt="avatar" />
    <div class="room-info">
      <div class="room-title-row">
        <h3>{{ room.name }}</h3>
        <span class="time">{{ formatTime(room.lastMessageTime) }}</span>
      </div>
      <div class="room-bottom-row">
        <p class="last-message">{{ room.lastMessage }}</p>
        <span v-if="room.unreadCount > 0" class="unread-dot"></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { format } from 'date-fns'
const props = defineProps({
  room: Object
})
function formatTime(timestamp) {
  const now = new Date()
  const messageDate = new Date(timestamp)
  if (now.toDateString() === messageDate.toDateString()) {
    return format(messageDate, 'HH:mm')
  }
  return format(messageDate, 'MM/dd')
}
</script>
<style scoped>
.chat-room-item {
  display: flex;
}
.chat-room-item:hover {
  background-color: #f0f0f0;
}
.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 12px;
  background: #e9e9e9;
}
.room-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}
.room-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.room-title-row h3 {
  margin: 0;
  font-size: 1.08rem;
  color: #222;
  font-weight: 700;
  max-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.time {
  font-size: 0.92rem;
  color: #A3C8FF;
  margin-left: 8px;
  min-width: 56px;
  text-align: right;  
}
.room-bottom-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 2px;
  min-width: 0;
}
.last-message {
  margin: 0;
  color: #666;
  font-size: 0.98rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
  flex-shrink: 1;
}
.unread-dot {
  width: 10px;
  height: 10px;
  background: #4F8CFF;
  border-radius: 50%;
  display: inline-block;
  margin-left: 10px;
}
</style> 