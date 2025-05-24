export const statusMapping = {
  'WELCOME': '歡迎',
  'IDLE': '等待備貨',
  'WAITING_OWNER': '人工溝通',
  'BOT_ACTIVE': '自動回覆'
}

export function getStatusDisplay(status) {
  return statusMapping[status] || status
}

export function getStatusClass(status) {
  switch (status) {
    case 'IDLE':
      return 'wait'
    case 'WAITING_OWNER':
      return 'manual'
    case 'BOT_ACTIVE':
      return 'auto'
    default:
      return ''
  }
} 