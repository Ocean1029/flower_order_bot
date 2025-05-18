<template>
  <div class="chat-room">
    <ChatHeader :roomName="roomName" :avatar="avatar" :status="status" @showDetail="$emit('showDetail')" />
    <MessageList :messages="messages" ref="messagesContainer" />
    <MessageInput v-model="newMessage" @send="handleSend" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import { getRoomMessages, sendMessage as apiSendMessage } from '@/api/messages'
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

async function loadMessages() {
  try {
    const response = await getRoomMessages(props.roomId)
    messages.value = response.map(msg => ({
      id: msg.id,
      sender: msg.direction === 'outgoing_by_staff' || msg.direction === 'outgoing_by_bot' ? '我' : props.roomName,
      text: msg.message.text,
      timestamp: new Date(msg.created_at),
      direction: msg.direction
    }))
    nextTick(() => {
      scrollToBottom()
    })
  } catch (error) {
    console.error('Error loading messages:', error)
  }
}

onMounted(loadMessages)
watch(() => props.roomId, loadMessages)

async function handleSend() {
  if (!newMessage.value.trim()) return
  
  try {
    // Send the message text to the backend
    await apiSendMessage(props.roomId, {
      text: newMessage.value,
      image_url: null
    })
    newMessage.value = ''
    await loadMessages() // Reload messages to get the latest state
  } catch (error) {
    console.error('Error sending message:', error)
  }
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
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
}
</style> 