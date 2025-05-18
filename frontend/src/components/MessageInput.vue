<template>
  <div class="input-container">
    <input
      v-model="inputValue"
      @keyup.enter="handleSend"
      placeholder="輸入訊息..."
      type="text"
    >
    <button @click="handleSend">發送</button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['update:modelValue', 'send'])
const inputValue = ref(props.modelValue || '')

// Watch for changes from parent
watch(() => props.modelValue, (newVal) => {
  inputValue.value = newVal
})

// Watch for changes to emit to parent
watch(inputValue, (newVal) => {
  emit('update:modelValue', newVal)
})

function handleSend() {
  if (!inputValue.value.trim()) return
  emit('send')
}
</script>

<style scoped>
.input-container {
  padding: 1rem;
  background-color: #fff;
  display: flex;
  gap: 0.5rem;
}
input {
  flex: 1;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 1.5rem;
  outline: none;
}
button {
  padding: 0.5rem 1.5rem;
  background-color: #007AFF;
  color: white;
  border: none;
  border-radius: 1.5rem;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style> 