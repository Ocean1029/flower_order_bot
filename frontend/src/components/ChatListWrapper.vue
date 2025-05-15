<template>
  <div class="chat-list">
    <div class="chatlist-tabs">
      <button
        v-for="tab in tabs"
        :key="tab"
        :class="['tab', { active: currentTab === tab }]"
        @click="currentTab = tab"
      >
        {{ tab }}
      </button>
    </div>
    <div class="chat-rooms">
      <ChatRoomItem
        v-for="room in filteredRooms"
        :key="room.id"
        :room="room"
        @click="selectRoom(room)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ChatRoomItem from './ChatRoomItem.vue'
const props = defineProps({
  chatRooms: Array
})
const emit = defineEmits(['selectRoom'])
function selectRoom(room) {
  emit('selectRoom', room)
}
const tabs = [
  '所有訂單',
  '人工溝通',
  '今日訂單',
  '等待備貨',
  '自動回復'
]
const currentTab = ref('所有訂單')
const filteredRooms = computed(() => {
  if (currentTab.value === '所有訂單') return props.chatRooms
  return props.chatRooms.filter(r => r.status === currentTab.value)
})
</script>

<style scoped>
.chat-list {
  height: 100vh;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
}
.chatlist-tabs {
  display: flex;
  gap: 8px;
  padding: 18px 0 8px 0;
  background: #fff;
  border-bottom: 1.5px solid #e9e9e9;
  justify-content: space-between;
}
.tab {
  background: none;
  border: none;
  font-size: 15px;
  font-weight: 700;
  color: #6168FC;
  padding: 8px 18px;
  border-radius: 16px 16px 0 0;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.tab.active {
  background: #eaf2ff;
  color: #4F8CFF;
}
.chat-rooms {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 0.5rem 0 0.5rem;
}
</style> 