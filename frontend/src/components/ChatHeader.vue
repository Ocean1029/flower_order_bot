<template>
  <div class="chat-header">
    <h2>{{ roomName }}</h2>
  </div>
</template>
<script setup>
const props = defineProps({
  roomName: String
})
</script>
<style scoped>
.chat-header {
  padding: 1rem;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style> 