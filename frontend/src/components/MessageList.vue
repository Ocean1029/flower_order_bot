<template>
  <div class="messages-container">
    <MessageItem
      v-for="message in messages"
      :key="message.id"
      :message="message"
    />
  </div>
</template>
<script setup>
import MessageItem from './MessageItem.vue'
const props = defineProps({
  messages: Array
})
</script>
<style scoped>
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}
</style> 