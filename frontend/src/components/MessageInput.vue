<template>
  <div class="messages-container">
    <div class="input-container">
      <div class="textbar" @click="focusInput">
        <div class="content">
          <i class="fas fa-paperclip attach-icon"></i>
          <input
            ref="inputRef"
            v-model="inputValue"
            @keyup.enter="emitSend"
            class="message-input"
            placeholder="輸入訊息......"
            type="text"
          >
        </div>
        <div class="send" @click="emitSend">
          <i class="fas fa-paper-plane send-icon"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
const props = defineProps({
  modelValue: String
})
const emit = defineEmits(['update:modelValue', 'send'])
const inputValue = ref(props.modelValue || '')
const inputRef = ref(null)
watch(() => props.modelValue, val => { inputValue.value = val })
function emitSend() {
  if (!inputValue.value.trim()) return
  emit('send')
}
watch(inputValue, val => emit('update:modelValue', val))
function focusInput() {
  inputRef.value && inputRef.value.focus()
}
</script>

<style scoped>
.input-container {
  position: absolute;
  left: 24px;
  right: 24px;
  bottom: 0;
  margin-bottom: 33px;
  padding: 0;
}

.textbar {
  width: 100%;
  height: 42px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 24px;
  padding: 9px 16px;
  border: 2px solid #77B5FF;
  box-shadow: 2px 2px 4px 0px #00000040;
  background: #fff;
  box-sizing: border-box;
  cursor: pointer;
}
.content {
  display: flex;
  align-items: center;
  width: 180px;
  height: 24px;
  gap: 12px;
}
.attach-icon {
  width: 11px;
  height: 20px;
  color: #528DD2;
  font-size: 20px;
  margin-right: 6px;
}
.message-input {
  width: 144px;
  height: 22px;
  border: none;
  outline: none;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 400;
  font-size: 16px;
  line-height: 140%;
  background: transparent;
  color: #000000DE;
  letter-spacing: 0;
  padding: 0;
}
.message-input::placeholder {
  color: #00000061;
}
.send {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.send-icon {
  width: 24px;
  height: 24px;
  color: #528DD2;
  font-size: 20px;
  margin-left: 3px;
  margin-top: 4px;
}
.messages-container {
  position: relative;
}
</style> 