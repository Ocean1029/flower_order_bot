<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">
        <i class="fas fa-store me-2"></i>花店管理平台
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/orders" class="nav-link" active-class="active" exact>訂單管理</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/messages" class="nav-link" active-class="active">對話記錄</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/stats" class="nav-link" active-class="active">數據統計</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>





<script setup>
// 無特別邏輯，純 UI
</script>
