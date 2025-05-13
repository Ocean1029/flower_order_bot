<template>
  <div class="page-content">
    <ChatRoomWrapper :roomId="roomId" :roomName="roomName" />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import ChatRoomWrapper from '@/components/ChatRoomWrapper.vue'

const route = useRoute()
const roomId = route.params.id
const roomName = route.state?.roomName || '聊天室'
</script> 