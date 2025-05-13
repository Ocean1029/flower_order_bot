<script setup>
import '@/assets/index.css'// 全域樣式
import Navbar from './components/Navbar.vue'
import OrderTitle from './components/OrderTitle.vue'
</script>

<template>
  <Navbar />
  <OrderTitle />
  <router-view />
</template>

<style>
:root {
  --primary: #4F8CFF;
  --primary-dark: #007AFF;
  --secondary: #A3C8FF;
  --accent: #7B61FF;
  --alert: #FF6F91;
  --success: #3DC9B3;
  --gray-100: #f5f6fa;
  --gray-200: #e9e9e9;
  --gray-300: #bdbdbd;
  --text-main: #222;
  --text-sub: #666;
  --text-light: #aaa;
}
body {
  font-family: 'Noto Sans TC', '思源黑體', 'Microsoft JhengHei', Arial, sans-serif;
  background: #f5f6fa;
  color: var(--text-main);
}

</style>


