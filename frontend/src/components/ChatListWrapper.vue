<template>
  <div class="chat-list">
    <!-- section：上方標題列 -->
    <div class="section">
      <div class="head">
        <!-- Icon Container -->
          <div class="message-circle">
            <i class="far fa-comment" style="color: #6168FC;"></i>
          </div>
        <!-- Title -->
        <span class="message-title">Message</span>
        <!-- Unread Count -->
        <div class="number-wrapper">
          <div class="ellipse"></div>
          <span class="number">{{ unreadCount }}</span>
        </div>
      </div>
    </div>

    <!-- content：聊天室列表 -->
    <div class="content"
      ref="contentRef"
      @scroll="handleScroll"
    >
      <!-- Filter bar -->
      <div class="filter-bar">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="['filter-btn', { active: currentTab === tab.key }]"
          @click="currentTab = tab.key"
        >
          <span class="filter-label">{{ tab.label }}</span>
        </button>
      </div>

      <!-- 聊天室卡片列表 -->
      <div
        v-for="room in filteredRooms"
        :key="room.id"
        class="customer-card-wrapper"
        :class="{ active: selectedRoomId === room.id }"
        @click="selectRoom(room)"
      >
        <div class="frame6">
          <!-- 頭像 -->
          <img class="pic" :src="room.avatar" alt="avatar" />

          <div class="frame5">
            <div class="frame4">
              <div class="frame3">
                <span class="name">{{ room.name }}</span>
                <span class="time">{{ formatTime(room.lastMessageTime) }}</span>
              </div>
              <div class="frame7">
                <span class="unread_text">{{ room.lastMessage }}</span>
                <span
                  v-if="room.unreadCount > 0 && selectedRoomId !== room.id"
                  class="unread_point"
                ></span>
              </div>
            </div>
            <div
              class="frame2"
              :class="statusClass(room.status)"
            >
              <span
                :class="['status-label', statusClass(room.status)]"
              >
                {{ getStatusDisplay(room.status) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { getStatusDisplay, getStatusClass } from '@/utils/statusMapping'

const props = defineProps({
  chatRooms: Array,
  selectedRoomId: String
})
const emit = defineEmits(['selectRoom', 'read'])

// 新增一個本地的 rooms 狀態，讓 unreadCount 可即時變動
const localRooms = ref(props.chatRooms.map(room => ({ ...room })))

watch(() => props.chatRooms, (newRooms) => {
  localRooms.value = newRooms.map(room => ({ ...room }))
})

function selectRoom(room) {
  // 點擊時將該聊天室的 unreadCount 設為 0
  const idx = localRooms.value.findIndex(r => r.id === room.id)
  if (idx !== -1) {
    localRooms.value[idx].unreadCount = 0
  }
  emit('selectRoom', room)
}

const tabs = [
  { key: 'WELCOME', label: '歡迎' },
  { key: 'ORDER_CONFIRM', label: '等待備貨' },
  { key: 'WAITING_OWNER', label: '人工溝通' },
  { key: 'BOT_ACTIVE', label: '自動回覆' }
]
const currentTab = ref('所有訂單')

const filteredRooms = computed(() => {
  if (currentTab.value === '所有訂單') return localRooms.value
  return localRooms.value.filter(r => r.status === currentTab.value)
})

const unreadCount = computed(() =>
  localRooms.value.reduce(
    (sum, room) =>
      sum + (room.unreadCount && props.selectedRoomId !== room.id ? room.unreadCount : 0),
    0
  )
)

function statusClass(status) {
  return getStatusClass(status)
}

function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const now = new Date()
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString('zh-TW', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    })
  }
  return `${date.getMonth() + 1}/${date.getDate()}`
}

const contentRef = ref(null)

function handleScroll() {
  // No need to update scroll bar manually as the native scrollbar will handle it
}

onMounted(() => {
  // No need to call nextTick as the native scrollbar will handle it
})
watch(filteredRooms, () => {
  // No need to call nextTick as the native scrollbar will handle it
})
</script>

<style scoped>
.chat-list {
  position: absolute;
  top: 56px;
  width: 360px;
  height: calc(100vh - 56px);
  background: #fff;
  border-right: 1px solid #B3B3B3;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

/* section */
.section {
  position: relative;
  width: 360px;
  height: 80px;
  margin-left: 0px;
  top: 0px;
  display: flex;
  align-items: center;
  border-bottom: 1.5px solid #e9e9e9;
  border-right: 1px solid #e9e9e9;
}
.head {
  position: absolute;
  height: 36px;
  top: 20px;
  left: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.message-circle {
  position: relative;
  top: 2px;
  left: 0px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;  
}  

.message-title {
  height: 30px;
  font-family: 'Noto Sans TC';
  font-weight: 700;
  font-size: 24px;
  line-height: 125%;
  letter-spacing: 0.1em;
  vertical-align: middle;
  color: #6168FC;
}

.number-wrapper {
  top: 2px;
  position: relative;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}  
.ellipse {
  position: absolute;
  width: 32px;
  height: 32px;
  background: #D8EAFF;  
  border-radius: 50%;
}
.number {
  position: relative;
  color: #528DD2;
  font-family: 'Noto Sans TC';
  font-weight: 700;
  font-size: 14px;
  line-height: 113%;
  letter-spacing: 0%;
  text-align: center;
  z-index: 1;
}

/* content */
.content {
  position: absolute;
  top: 80px;
  left: 0;
  width: 360px;
  height: calc(100vh - 56px - 80px);
  overflow-y: auto;
  overflow-x: hidden;
  flex: 1;
  scrollbar-width: thin;
  scrollbar-color: #E4E4E4 #F7F7F7;
}
.content::-webkit-scrollbar {
  width: 8px;
  background: #F7F7F7;
}
.content::-webkit-scrollbar-thumb {
  background: #E4E4E4;
  border-radius: 12px;
}
.content::-webkit-scrollbar-track {
  background: #F7F7F7;
  border-radius: 12px;
}

/* filter bar */
.filter-bar {
  position: relative;
  width: 360px;
  height: 40px;
  background: #F7F7F7;
  display: flex;
  align-items: center;
  overflow-x: auto;
  overflow-y: hidden;
  white-space: nowrap;
  scrollbar-width: thin;
  scrollbar-color: #E4E4E4 #F7F7F7;
  box-sizing: border-box;
  gap: 4px;
  padding: 6px 12px 6px 12px;
}
.filter-btn {
  width: 72px;
  height: 28px;
  border-radius: 36px;
  background: #F7F7F7;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 11px 8px;
  margin-right: 12px;
  white-space: nowrap;
  transition: background 0.2s;
}
.filter-btn:last-child {
  margin-right: 0;
}
.filter-btn.active,
.filter-btn:hover {
  background: #C5C7FF;
}

/* customer cards */
.customer-card-wrapper {
  width: 360px;
  height: 100px;
  border-radius: 12px;
  background: transparent;
  transition: background 0.2s;
  display: flex;
  align-items: center;
}

/* 被選取時（active） */
.customer-card-wrapper.active {
  background: #D8EAFF;
}

.frame6 {
  display: flex;
  align-items: center;
  width: 327;
  height: 74px;
  margin-left: 17px;
  gap: 16px;
}
.pic {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  object-fit: cover;
}

.frame5 {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 74px;
  width: 255px;
  gap: 8px;
}
.frame4 {
  display: flex;
  flex-direction: column;
  height: 46px;
  width: 255px;
  gap: 4px;
}
.frame3 {
  display: flex;
  justify-content: space-between;
  height: 22px;
  width: 255px;
  align-items: center;
}
.frame7 {
  display: flex;
  justify-content: space-between;
  height: 22px;
  width: 255px;
  align-items: center;
  padding-right: 8px;
}
.name {
  font-family: 'Noto Sans TC';
  font-weight: 700;
  font-size: 16px;
  height: 22px;
  line-height: 140%;
  color: #000;
}
.time {
  font-family: 'Noto Sans TC';
  font-weight: 700;
  font-size: 16px;
  height: 22px;
  line-height: 140%;
  color: #00000061;
}
.unread_text {
  font-family: 'Noto Sans TC';
  font-weight: 400;
  width: 90%;
  font-size: 14px;
  height: 20px;
  line-height: 140%;
  color: #00000099;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex-shrink: 1;
}
.unread_point {
  width: 12px;
  height: 12px;
  background: #77B5FF;
  border-radius: 50%;  
}
.frame2.welcome { background: #FFCEE7; }
.frame2.auto { background: #D8EAFF; }
.frame2.wait { background: #C5C7FF; }
.frame2.prepare { background: #EBCDCC; }
.frame2 {
  display: flex;
  align-items: center;
  width: 72px;
  height: 20px;
  gap: 10px;
  border-radius: 12px;
  /* 其他你要的設定 */
}

.status-label.welcome { color: #FF349A; background: transparent; }
.status-label.auto { color: #528DD2; background: transparent; }
.status-label.wait { color: #6168FC; background: transparent; }
.status-label.prepare { color: #81386A; background: transparent; }

.status-label {
  font-family: 'Noto Sans TC';
  font-weight: 700;
  font-size: 12px;
  line-height: 113%;
  letter-spacing: 0%;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 12px;
  width: 100%;
  height: 100%;
}

.filter-bar::-webkit-scrollbar {
  height: 6px;
}
.filter-bar::-webkit-scrollbar-thumb {
  background: #E4E4E4;
  border-radius: 3px;
}

.filter-label {
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 700;
  font-size: 14px;
  line-height: 113%;
  letter-spacing: 0%;
  vertical-align: middle;
  color: #00000099;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}
</style>
