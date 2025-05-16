<template>
    <div class="chat-main-layout">
      <!-- 左側聊天室列表 -->
      <div class="chat-list-panel">
        <ChatListWrapper
          :chatRooms="chatRooms"
          @selectRoom="selectRoom"
          :selectedRoomId="selectedRoom?.id"
        />
      </div>
      <!-- 中間訊息區 -->
      <div class="chat-room-panel" :class="{ expanded: !showDetailPanel }" v-if="selectedRoom">
        <ChatRoomWrapper
          :roomId="selectedRoom.id"
          :roomName="selectedRoom.name"
          :avatar="selectedRoom.avatar"
          :status="selectedRoom.status"
          @showDetail="showDetailPanel = true"
        />
      </div>
      <!-- 右側詳細資料 -->
      <div class="chat-detail-panel" v-if="selectedRoom && showDetailPanel">
        <DetailPanel
          :room="selectedRoom"
          @close="showDetailPanel = false"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import ChatListWrapper from '@/components/ChatListWrapper.vue'
  import ChatRoomWrapper from '@/components/ChatRoomWrapper.vue'
  import DetailPanel from '@/components/DetailPanel.vue'
  import { mockChatRooms } from '@/mockData'
  
  const chatRooms = ref([])
  const selectedRoom = ref(null)
  const showDetailPanel = ref(false)
  
  onMounted(() => {
    chatRooms.value = mockChatRooms
    selectedRoom.value = chatRooms.value[0] // 預設選第一個
  })
  
  function selectRoom(room) {
    selectedRoom.value = room
    showDetailPanel.value = false // 切換聊天室時自動收起詳細資料
  }
</script>

<style scoped>
.chat-main-layout {
  display: flex;
  height: calc(100vh - 80px); /* 80px Navbar*/
  margin-top: 160px;
}
.chat-list-panel {
  width: 320px;
  border-right: 1px solid #e9e9e9;
  background: #f5f5f5;
  overflow-y: auto;
}
.chat-room-panel {
  flex: 1;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
}
.chat-room-panel.expanded {
  width: calc(100vw - 320px);
}
.chat-detail-panel {
  width: 340px;
  background: #fff;
  border-left: 1px solid #e9e9e9;
  padding: 24px;
  overflow-y: auto;
  transition: width 0.3s;
}
</style>
