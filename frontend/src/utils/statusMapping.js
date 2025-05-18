export const statusMapping = {
  'welcome': '自動回覆',
  'idle': '等待對方回覆',
  'waiting_owner': '人工溝通',
  'bot_active': '自動回覆',
  'order_confirm':'已經下訂'
}

export function getStatusDisplay(status) {
  return statusMapping[status] || status
}

export function getStatusClass(status) {
  switch (status) {
    case 'idle':
      return 'wait'
    case 'waiting_owner':
      return 'manual'
    case 'bot_active':
      return 'auto'
    default:
      return ''
  }
} 