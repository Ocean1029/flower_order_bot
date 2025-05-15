<template>
  <div class="chat-room">
    <ChatHeader :roomName="roomName" :avatar="avatar" :status="status" @showDetail="$emit('showDetail')" />
    <MessageList :messages="messages" ref="messagesContainer" />
    <MessageInput v-model="newMessage" @send="sendMessage" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import { mockChatMessages } from '@/mockData'
import ChatHeader from './ChatHeader.vue'
import MessageList from './MessageList.vue'
import MessageInput from './MessageInput.vue'

const props = defineProps({
  roomId: String,
  roomName: String,
  avatar: String,
  status: String
})
const emit = defineEmits(['showDetail'])
const messages = ref([])
const newMessage = ref('')
const messagesContainer = ref(null)

function loadMessages() {
  messages.value = mockChatMessages[props.roomId] || []
}

onMounted(loadMessages)
watch(() => props.roomId, loadMessages)

function sendMessage() {
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
function scrollToBottom() {
  if (messagesContainer.value && messagesContainer.value.$el) {
    messagesContainer.value.$el.scrollTop = messagesContainer.value.$el.scrollHeight
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
</style> 