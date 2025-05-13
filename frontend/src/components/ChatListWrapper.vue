<template>
  <div class="chat-list">
    <div class="header">
      <h1>聊天室列表</h1>
    </div>
    <div class="chat-rooms">
      <ChatRoomItem
        v-for="room in chatRooms"
        :key="room.id"
        :room="room"
        @click="selectRoom(room)"
      />
    </div>
  </div>
</template>

<script setup>
import ChatRoomItem from './ChatRoomItem.vue'
const props = defineProps({
  chatRooms: Array
})
const emit = defineEmits(['selectRoom'])
function selectRoom(room) {
  emit('selectRoom', room)
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
</style> 