<template>
  <div class="navbar-wrapper">
    <!-- 品牌區塊 -->
    <div class="brand-bar">
      <i class="fas fa-store-alt brand-icon"></i>
      <span class="brand-title">奇美花店 <b>Chi-Mei Floral</b></span>
    </div>
    <!-- routing bar -->
    <nav class="routing-bar">
      <router-link to="/" class="routing-title" active-class="active-title">
        <i class="fas fa-store me-2"></i>訂單管理平台
      </router-link>
      <div class="routing-links">
        <router-link to="/orders" class="nav-link" active-class="active">訂單管理</router-link>
        <router-link to="/messages" class="nav-link" active-class="active">對話記錄</router-link>
        <router-link to="/stats" class="nav-link" active-class="active">數據統計</router-link>
      </div>
    </nav>
  </div>
</template>

<script setup>
// 無特別邏輯，純 UI
</script>

<style scoped>
.navbar-wrapper {
  width: 100%;
  margin-bottom: 32px;
}
.brand-bar {
  width: 100%;
  background: linear-gradient(90deg, #4F8CFF 0%, #7B61FF 100%);
  border-radius: 16px 16px 0 0;
  padding: 18px 40px 16px 40px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 16px rgba(79,140,255,0.10);
}
.brand-icon {
  font-size: 2rem;
  color: #fff;
  margin-right: 10px;
}
.brand-title {
  color: #fff;
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: 1px;
}
.routing-bar {
  width: 100%;
  background: linear-gradient(90deg, #4F8CFF 0%, #7B61FF 100%);
  border-radius: 0 0 20px 20px;
  padding: 18px 40px 16px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 24px rgba(79,140,255,0.10);
}
.routing-title {
  color: #2979FF;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 8px;
  padding: 6px 24px;
  box-shadow: 0 2px 8px rgba(79,140,255,0.08);
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
  border: 2px solid #4F8CFF;
}
.routing-title:hover, .routing-title.active-title {
  background: #eaf2ff;
  color: #007AFF;
}
.routing-links {
  display: flex;
  gap: 32px;
}
.nav-link {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 6px 18px;
  border-radius: 8px;
  transition: background 0.2s, color 0.2s;
  text-decoration: none;
}
.nav-link.active, .nav-link:hover {
  background: rgba(255,255,255,0.18);
  color: #fff;
}
</style>
