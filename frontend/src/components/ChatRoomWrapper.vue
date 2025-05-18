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
      <MessageInput v-model="newMessage" @send="sendMessage" />
    </div>    
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
  status: String,
  showDetail: Boolean
})
const emit = defineEmits(['showDetail', 'open-detail'])
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
  height: 100%;
  background-color: #ffffff;
  border-right: 1px solid #B3B3B3;
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