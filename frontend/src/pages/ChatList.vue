<template>
  <div class="chat-list">
    <div class="header">
      <h1>聊天室列表</h1>
    </div>
    
    <div class="chat-rooms">
      <div v-for="room in chatRooms" 
           :key="room.id" 
           class="chat-room-item"
           @click="navigateToChat(room)">
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
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { format } from 'date-fns'

const router = useRouter()

// 模擬聊天室數據
const chatRooms = ref([
  {
    id: '1',
    name: '客服中心',
    lastMessage: '您好，有什麼可以幫您的嗎？',
    lastMessageTime: new Date(),
    unreadCount: 2
  },
  {
    id: '2',
    name: '訂單查詢',
    lastMessage: '您的訂單已經出貨',
    lastMessageTime: new Date(Date.now() - 3600000),
    unreadCount: 0
  },
  {
    id: '3',
    name: '商品諮詢',
    lastMessage: '這個商品還有庫存嗎？',
    lastMessageTime: new Date(Date.now() - 86400000),
    unreadCount: 1
  }
])

const formatTime = (timestamp) => {
  const now = new Date()
  const messageDate = new Date(timestamp)
  
  if (now.toDateString() === messageDate.toDateString()) {
    return format(messageDate, 'HH:mm')
  }
  return format(messageDate, 'MM/dd')
}

const navigateToChat = (room) => {
  router.push({
    name: 'chat-room',
    params: { id: room.id },
    state: { roomName: room.name }
  })
}
</script>

<style scoped>
.chat-list {
  height: 100vh;
  background-color: #f5f5f5;
}

.header {
  padding: 1rem;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.chat-rooms {
  padding: 0.5rem;
}

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