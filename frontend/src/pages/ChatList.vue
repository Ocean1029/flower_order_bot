<template>
  <ChatListWrapper :chatRooms="chatRooms" @selectRoom="goToRoom" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { mockChatRooms } from '@/mockData'
import ChatListWrapper from '@/components/ChatListWrapper.vue'

const router = useRouter()
const chatRooms = ref([])

onMounted(() => {
  chatRooms.value = mockChatRooms
})

const goToRoom = (room) => {
  router.push({
    name: 'chat-room',
    params: { id: room.id },
    state: { roomName: room.name }
  })
}
</script> 