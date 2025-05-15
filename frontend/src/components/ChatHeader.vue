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
  width: 40px;
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
</style> 