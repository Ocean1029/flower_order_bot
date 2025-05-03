<script setup>
import ConversationList from '@/components/ConversationList.vue'
import { onMounted, ref } from 'vue'
import { getLatestMessages } from '@/api/messages'

const messages = ref([])

onMounted(async () => {
  try {
    messages.value = await getLatestMessages()
  } catch (err) {
    console.error('無法取得訊息資料', err)
  }
})
</script>

<template>
  <div>
    <ConversationList :messages="messages" />
  </div>
</template>
