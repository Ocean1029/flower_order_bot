<template>
  <!-- 半透明遮罩層，點擊也可關閉 -->
  <transition name="fade">
    <div class="overlay" v-if="show" @click="$emit('close')" />
  </transition>

  <!-- 側邊欄本體，用 slide 動畫從左邊滑進來 -->
  <transition name="sidebar">
    <aside class="sidebar" v-if="show">
      <header class="sidebar-header">
        <h2>訂單管理平台</h2>
        <button class="close-btn" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </header>
      <nav class="sidebar-menu">
        <ul>
          <li v-for="item in menu" :key="item.label" @click="select(item)" :class="{ active: active === item.label }">
            <i :class="item.icon"></i> {{ item.label }}
          </li>
        </ul>
      </nav>
    </aside>
  </transition>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({ show: Boolean })
const emit  = defineEmits(['close'])

const router = useRouter()
const menu = [
  { label: '首頁', icon: 'fas fa-home',        route: '/' },
  { label: '訂單管理', icon: 'fas fa-shopping-bag', route: '/orders' },
  { label: '顧客溝通', icon: 'fas fa-comment',     route: '/messages' },
  { label: '統計資料', icon: 'fas fa-chart-bar',   route: '/stats' }
]
const active = ref(menu[0].label)

function select(item) {
  active.value = item.label
  router.push(item.route)
  emit('close')
}
</script>

<style scoped>
/* 遮罩 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}

/* 滑動動畫 */
.sidebar-enter-active,
.sidebar-leave-active {
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.sidebar-enter-from {
  transform: translateX(-100%);
}
.sidebar-enter-to {
  transform: translateX(0);
}
.sidebar-leave-from {
  transform: translateX(0);
}
.sidebar-leave-to {
  transform: translateX(-100%);
}

/* 遮罩層 */
.overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.4);
  z-index: 999;
}

/* 側邊欄樣式 */
.sidebar {
  position: fixed;
  top: 0; left: 0;
  width: 280px; height: 100vh;
  background: #F7F7F7;
  box-shadow: 2px 0 12px rgba(0,0,0,0.2);
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 標頭 */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 56px;
  background: #f5f5f5;
  border-bottom: 1px solid #00000061; /* ← 分隔線 */
}

.sidebar-header h2 {
  height: 25px;
  top: 26px;
  left: 30px;
  margin: 0;
  font-size: 18px;
  color: #6168FC;
}
.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #333;
}

/* 選單 */
.sidebar-menu {
  padding: 20px 0;
  flex: 1;
  overflow-y: auto;
}
.sidebar-menu ul {
  list-style: none;
  margin: 0; padding: 0;
}
.sidebar-menu li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  font-size: 16px;
  color: #555;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.sidebar-menu li:hover,
.sidebar-menu li.active {
  background: #e4e7ff;
  color: #4f68ff;
}
.sidebar-menu i {
  width: 20px;
  text-align: center;
}
</style>
