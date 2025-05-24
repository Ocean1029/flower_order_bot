<template>
  <div :class="['chat-room', { shrink: showDetail }]">
    <ChatHeader :roomName="roomName" :avatar="avatar" :status="status" @showDetail="$emit('showDetail')" />

    <!-- 這裡包一層可捲動容器 -->
    <div class="message-list-container">
      <MessageList
        :messages="messages"
        ref="messagesContainer"
      />
    </div>
    <div class="input-wrapper">
      <MessageInput v-model="newMessage" @send="handleSend" />
    </div>    
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
  status: String,
  showDetail: Boolean
})

const emit = defineEmits(['showDetail', 'open-detail'])
const messages = ref([])
const newMessage = ref('')
const messagesContainer = ref(null)

async function loadMessages() {
  try {
    const response = await getRoomMessages(props.roomId)
    messages.value = response.map(msg => ({
      id: msg.id,
      sender: msg.direction === 'OUTGOING_BY_STAFF' || msg.direction === 'OUTGOING_BY_BOT' ? '我' : props.roomName,
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
    await apiSendMessage(props.roomId, {
      text: newMessage.value
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
  background-color: #ffffff;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;    
  overflow: hidden;
  scrollbar-width: thin;
  scrollbar-color: #E4E4E4 #F7F7F7;
}

/* 這裡讓訊息列表填滿中間並可滾動 */
.message-list-container {
  flex: 1;
  overflow-y: auto;
}

.input-wrapper {
  flex: none;
}
</style> 