<template>
  <div class="navbar-wrapper">
    <div class="brand-bar">
      <button class="hamburger-btn" @click="showSidebar = true">
        <i class="fas fa-bars"></i>
      </button>
      <span class="brand-title">奇美花店 <b>Chi-Mei Floral</b></span>
    </div>
    <Sidebar :show="showSidebar" @close="showSidebar = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './Sidebar.vue'
const showSidebar = ref(false)
</script>

<style scoped>
.navbar-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 56px;
  display: flex;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  z-index: 1000;
}

.brand-bar {
  position: relative;
  width: 100%;
  height: 56px;
  border-radius: 24px;
  background: linear-gradient(90.11deg, #6168FC 5.18%, #77B5FF 98.9%);
}

.hamburger-btn {
  position: relative;
  top: 13px;
  left: 28px;
  width: 32px;
  height: 32px;
  background: none;
  border: none;
  color: #fff;
  font-size: 28px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.brand-title {
  position: absolute;
  top: 13px;
  left: 73px;
  height: 30px;
  display: flex;
  align-items: center;
  gap: 13px;
  color: #fff;
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: 3px;
}
</style>
