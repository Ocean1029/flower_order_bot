<template>
  <div class="chat-room-item" @click="$emit('click')">
    <div class="room-info">
      <h3>{{ room.name }}</h3>
      <p class="last-message">{{ room.lastMessage }}</p>
    </div>
    <div class="room-meta">
      <span class="time">{{ formatTime(room.lastMessageTime) }}</span>
      <span v-if="room.unreadCount" class="unread-badge">
        {{ room.unreadCount }}
      </span>
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
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #fff;
  margin-bottom: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.chat-room-item:hover {
  background-color: #f0f0f0;
}
.room-info {
  flex: 1;
}
.room-info h3 {
  margin: 0 0 0.25rem 0;
  color: #333;
}
.last-message {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}
.room-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}
.time {
  font-size: 0.8rem;
  color: #999;
}
.unread-badge {
  background-color: #007AFF;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  min-width: 1.5rem;
  text-align: center;
}
</style> 