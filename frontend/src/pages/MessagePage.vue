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
          :showDetail="showDetailPanel"
          @showDetail="showDetailPanel = true"
        />
      </div>
      <!-- 右側詳細資料 -->
      <div class="chat-detail-panel" v-if="selectedRoom && showDetailPanel">
        <DetailPanel
          :room="selectedRoom"
          @close-detail="showDetailPanel = false"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { getLatestMessages } from '@/api/messages'
  import ChatListWrapper from '@/components/ChatListWrapper.vue'
  import ChatRoomWrapper from '@/components/ChatRoomWrapper.vue'
  import DetailPanel from '@/components/DetailPanel.vue'

  const chatRooms = ref([])
  const selectedRoom = ref(null)
  const showDetailPanel = ref(false)
  
  async function loadChatRooms() {
    try {
      const response = await getLatestMessages()
      chatRooms.value = response
      if (chatRooms.value.length > 0 && !selectedRoom.value) {
        selectedRoom.value = chatRooms.value[0]
      }
    } catch (error) {
      console.error('Error loading chat rooms:', error)
    }
  }
  
  onMounted(loadChatRooms)
  
  function selectRoom(room) {
    selectedRoom.value = room
    showDetailPanel.value = false // 切換聊天室時自動收起詳細資料
  }
</script>

<style scoped>
.chat-main-layout {
  display: flex;
  margin-top: 56px;
  height: calc(100vh - 56px);
}
.chat-list-panel {
  width: 360px;
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
