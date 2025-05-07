<template>
  <div class="chat-room">
    <div class="chat-header">
      <h2>{{ roomName }}</h2>
    </div>
    
    <div class="messages-container" ref="messagesContainer">
      <div v-for="message in messages" :key="message.id" 
           :class="['message', message.isSelf ? 'self' : 'other']">
        <div class="message-content">
          <div class="message-sender">{{ message.sender }}</div>
          <div class="message-text">{{ message.text }}</div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
        </div>
      </div>
    </div>

    <div class="input-container">
      <input 
        v-model="newMessage" 
        @keyup.enter="sendMessage"
        placeholder="輸入訊息..."
        type="text"
      >
      <button @click="sendMessage">發送</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { format } from 'date-fns'

const props = defineProps({
  roomId: {
    type: String,
    required: true
  },
  roomName: {
    type: String,
    required: true
  }
})

const messages = ref([])
const newMessage = ref('')
const messagesContainer = ref(null)

// 模擬訊息數據
const mockMessages = [
  {
    id: 1,
    sender: '鄭博宇',
    text: '嗨',
    timestamp: new Date(),
    isSelf: false
  },
  {
    id: 2,
    sender: '我',
    text: '略略略',
    timestamp: new Date(),
    isSelf: true
  }
]

onMounted(() => {
  // 模擬載入訊息
  messages.value = mockMessages
  scrollToBottom()
})

const formatTime = (timestamp) => {
  return format(new Date(timestamp), 'HH:mm')
}

const sendMessage = () => {
  if (!newMessage.value.trim()) return

  const message = {
    id: Date.now(),
    sender: '我',
    text: newMessage.value,
    timestamp: new Date(),
    isSelf: true
  }

  messages.value.push(message)
  newMessage.value = ''
  
  nextTick(() => {
    scrollToBottom()
  })
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.chat-room {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.chat-header {
  padding: 1rem;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

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

.input-container {
  padding: 1rem;
  background-color: #fff;
  display: flex;
  gap: 0.5rem;
}

input {
  flex: 1;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 1.5rem;
  outline: none;
}

button {
  padding: 0.5rem 1.5rem;
  background-color: #007AFF;
  color: white;
  border: none;
  border-radius: 1.5rem;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style> 