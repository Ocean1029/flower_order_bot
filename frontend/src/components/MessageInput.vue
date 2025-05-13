<template>
  <div class="input-container">
    <input
      v-model="inputValue"
      @keyup.enter="emitSend"
      placeholder="輸入訊息..."
      type="text"
    >
    <button @click="emitSend">發送</button>
  </div>
</template>
<script setup>
import { ref, watch } from 'vue'
const props = defineProps({
  modelValue: String
})
const emit = defineEmits(['update:modelValue', 'send'])
const inputValue = ref(props.modelValue || '')
watch(() => props.modelValue, val => { inputValue.value = val })
function emitSend() {
  if (!inputValue.value.trim()) return
  emit('send')
}
watch(inputValue, val => emit('update:modelValue', val))
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