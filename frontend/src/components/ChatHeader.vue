<template>
  <div class="chat-header">
    <img class="avatar" :src="avatar" alt="avatar" />
      <div class="header-title-row">
        <span class="room-name">{{ roomName }}</span>
        <span
          class="status-badge"
          :class="statusClass"
        >
          {{ getStatusDisplay(status) }}
        </span>
        <button class="back-btn" @click="handleBackClick">
          <i class="fas fa-angle-double-left"></i>
        </button>        
      </div>
    <button class="order-btn" @click="handleOrderClick">
      <span class="icon">
        <span class="archive">
          <span class="archive-icon">
          <!-- 這裡可放 svg 或 fontawesome icon -->
            <i class="fas fa-archive"></i>
          </span>
        </span>
      </span>
      <span class="order-btn-text">整理資料</span>
    </button>   
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { getStatusDisplay, getStatusClass } from '@/utils/statusMapping'
import { fetchOrderDraft, readOrderDraft } from '@/api/orders'

const props = defineProps({
  roomName: String,
  avatar: String,
  status: String,
  roomId: String
})

const emit = defineEmits(['showDetail', 'orderDraftFetched'])

const statusClass = computed(() => getStatusClass(props.status))

const handleBackClick = async () => {
  try {
    console.log('Reading order draft for room:', props.roomId)
    const data = await readOrderDraft(props.roomId)
    console.log('Order draft data:', data)
    if (data && Object.keys(data).length > 0) {
      emit('orderDraftFetched', data)
    }
    emit('showDetail')
  } catch (error) {
    console.error('Error reading order draft:', error)
    emit('showDetail')
  }
}

const handleOrderClick = async () => {
  try {
    console.log('Fetching order draft for room:', props.roomId)
    const data = await fetchOrderDraft(props.roomId)
    console.log('Order draft data:', data)
    if (data && Object.keys(data).length > 0) {
      emit('orderDraftFetched', data)
    } else {
      alert('此聊天室尚未有訂單資料，請先建立訂單')
    }
  } catch (error) {
    console.error('Error fetching order draft:', error)
    alert('Error fetching order draft: ' + error.message)
  }
}
</script>

<style scoped>
.chat-header {
  display: flex;
  align-items: center;
  background-color: #fff;
  height: 80px;
  border-bottom: 1.5px solid #e9e9e9;

}
.back-btn {
  width: 16;
  height: 13.3;
  top: 9.33px;
  left: 8px;
  border: none;
  background: none;
  color: #00000099;
  font-size: 22px;
  margin-right: 16px;
  cursor: pointer;
  padding: 4px 8px;
}
.avatar {
  height: 56px;
  width: 56px;
  border-radius: 50%;
  object-fit: cover;
  margin-left: 51px;
  background: #e9e9e9;
}
.header-title-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: 16px;
}
.room-name {
  font-size: 1.15rem;
  font-weight: 700;  
  color: #6168FC;
}
.status-badge {
  height: 20px;
  max-width:92px;
  border-radius: 12px;
  padding: 0 15px;
  font-family: Noto Sans TC;
  font-weight: 700;
  font-size: 12px;
  line-height: 113%;
  letter-spacing: 0%;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
.order-btn {
  width: 119px;
  height: 40px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-radius: 12px;
  padding: 8px;
  background: #C5C7FF;
  color: #ffffff;
  border: none;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  box-sizing: border-box;
  margin-left: auto;
  margin-right: 24px;
}
.order-btn:hover {
  background: #C5C7FF;
  box-shadow: 2px 2px 2px 0px #00000040;

}
.icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.archive {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.archive-icon {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 3px;
  margin-top: 3px;
  /* 這裡可放svg或icon字體 */
}
.order-btn-text {
  height: 18px;
  font-family: 'Noto Sans TC';
  font-weight: 700;
  font-size: 16px;
  line-height: 113%;
  letter-spacing: 0;
  vertical-align: middle;
  color: #ffffff;
  display: flex;
  align-items: center;
  border-radius: 4px;
}
.message-section {
  width: 662px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #00000061;
  background: #fff;
  position: relative;
}

.frame8 {
  width: 300px;
  height: 80px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: 24px;
}

.customer {
  width: 248px;
  height: 80px;
  border-radius: 12px;
  border-bottom: 0.5px solid #B3B3B3;
  display: flex;
  align-items: center;
}

.frame6 {
  width: 215px;
  height: 56px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: 17px;
}

.pic {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #D9D9D9;
}

.frame5 {
  width: 143px;
  height: 25px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.customer-name {
  font-family: 'Noto Sans TC';
  font-weight: 700;
  font-size: 18px;
  line-height: 140%;
  background: #3138D7;
  color: #fff;
  height: 25px;
  display: flex;
  align-items: center;
  padding: 0 8px;
  border-radius: 6px;
}

.status-label.manual {
  width: 72px;
  height: 20px;
  max-width: 92px;
  border-radius: 12px;
  padding: 6px 15px;
  font-family: 'Noto Sans TC';
  font-weight: 700;
  font-size: 12px;
  line-height: 113%;
  text-align: center;
  vertical-align: middle;
  color: #FF349A;
  background: #FFCEE7;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.detail-button {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chevrons-left {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 2px;
  margin-top: 2px;
}

.chevrons-icon {
  width: 16px;
  height: 13.33px;
  border-left: 3px solid #00000099;
  border-bottom: 3px solid #00000099;
  border-radius: 2px;
  transform: rotate(45deg);
  margin-left: 8px;
  margin-top: 9.33px;
  display: inline-block;
}

.bottom {
  width: 119px;
  height: 40px;
  position: absolute;
  top: 20px;
  left: 519px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-radius: 12px;
  padding: 8px;
  background: #C5C7FF;
  box-shadow: 2px 2px 2px 0px #00000040;
  border: none;
  cursor: pointer;
}

.bottom-text {
  height: 18px;
  font-family: 'Noto Sans TC';
  font-weight: 700;
  font-size: 16px;
  line-height: 113%;
  letter-spacing: 0;
  vertical-align: middle;
  background: #fff;
  color: #3138D7;
  display: flex;
  align-items: center;
  padding: 0 4px;
  border-radius: 4px;
}

.status-badge.manual { color: #FF349A; background: #FFCEE7; }
.status-badge.auto { color: #528DD2; background: #D8EAFF; }
.status-badge.wait { color: #6168FC; background: #C5C7FF; }
.status-badge.done { color: #81386A; background: #EBCDCC; }
</style> 