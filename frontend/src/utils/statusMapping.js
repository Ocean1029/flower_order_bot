export const statusMapping = {
  'WELCOME': '歡迎',
  'ORDER_CONFIRM': '等待備貨',
  'WAITING_OWNER': '人工溝通',
  'BOT_ACTIVE': '自動回覆'
}

export function getStatusDisplay(status) {
  return statusMapping[status] || status
}

export function getStatusClass(status) {
  switch (status) {
    case 'ORDER_CONFIRM':
      return 'prepare'
    case 'WAITING_OWNER':
      return 'wait'
    case 'BOT_ACTIVE':
      return 'auto'
    case 'WELCOME':
      return 'welcome'
    default:
      return ''
  }
} 