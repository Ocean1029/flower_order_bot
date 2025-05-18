<template>
  <div class="chat-header">
    <button class="back-btn" @click="$emit('showDetail')">
      <i class="fas fa-angle-double-left"></i>
    </button>
    <img class="avatar" :src="avatar" alt="avatar" />
    <div class="header-info">
      <div class="header-title-row">
        <span class="room-name">{{ roomName }}</span>
        <span class="status-badge">{{ status }}</span>
      </div>
    </div>
    <button class="order-btn">整理訂單</button>
  </div>
</template>

<script setup>
const props = defineProps({
  roomName: String,
  avatar: String,
  status: String
})
</script>

<style scoped>
.chat-header {
  display: flex;
  align-items: center;
  padding: 0 18px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  height: 64px;
  border-bottom: 1.5px solid #e9e9e9;
}
.back-btn {
  background: none;
  border: none;
  color: #6168FC;
  font-size: 22px;
  margin-right: 16px;
  cursor: pointer;
  padding: 4px 8px;
}
.avatar {
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 14px;
  background: #e9e9e9;
}
.header-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}
.header-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}
.room-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: #222;
}
.status-badge {
  font-size: 0.95rem;
  color: #fff;
  background: #4F8CFF;
  border-radius: 12px;
  padding: 2px 12px;
  font-weight: 600;
}
.order-btn {
  margin-left: auto;
  background: #eaf2ff;
  color: #4F8CFF;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 700;
  padding: 8px 18px;
  cursor: pointer;
  transition: background 0.2s;
}
.order-btn:hover {
  background: #d0e4ff;
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
  background: #fff;
  border-radius: 4px;
  margin-left: 3px;
  margin-top: 3px;
  /* 這裡可放svg或icon字體 */
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
</style> 