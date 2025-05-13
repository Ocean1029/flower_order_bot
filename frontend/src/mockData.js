export const mockOrders = [
  {
    '訂單編號': '20250213011',
    '狀態': '自動回覆',
    '姓名': '愛兒堡',
    '電話': '0912345678',
    '品項': 'Nan',
    '數量': 1,
    '備註': '白色包材',
    '取貨方式': '店取',
    '取貨時間': 'Nan',
    '金額': 800,
    '付款方式': 'Line Pay'
  },
  {
    '訂單編號': '20250201019',
    '狀態': '人工溝通',
    '姓名': '曾海洋',
    '電話': '0912345678',
    '品項': '玫瑰花束',
    '數量': 1,
    '備註': '兩種顏色',
    '取貨方式': '店取',
    '取貨時間': '2025/02/05 16:00',
    '金額': 600,
    '付款方式': '匯款'
  },
  {
    '訂單編號': '20250202002',
    '狀態': '人工溝通',
    '姓名': '美女',
    '電話': '0912345678',
    '品項': '隨意',
    '數量': 2,
    '備註': '漂亮的那種',
    '取貨方式': '店取',
    '取貨時間': 'Nan',
    '金額': 2500,
    '付款方式': '匯款'
  },
  {
    '訂單編號': '20250207013',
    '狀態': '等待備貨',
    '姓名': 'chc',
    '電話': '0912345678',
    '品項': '滿天星+花',
    '數量': 1,
    '備註': '藍色系',
    '取貨方式': '指定地點',
    '取貨時間': '2025/02/10 16:00',
    '金額': 1200,
    '付款方式': '到店付款'
  },
  {
    '訂單編號': '20250205034',
    '狀態': '訂單完成',
    '姓名': '曾Amy',
    '電話': '0912345678',
    '品項': '康乃馨',
    '數量': 2,
    '備註': '要綁緞帶',
    '取貨方式': '店取',
    '取貨時間': '2025/02/09 14:00',
    '金額': 1000,
    '付款方式': '到店付款'
  }
];

export const mockMessages = [
  {
    id: 1,
    customer_name: "王小明",
    phone: "0912345678",
    preview: "我想訂兩束玫瑰花，預算2000元",
    time: "2024-03-20 10:30"
  },
  {
    id: 2,
    customer_name: "李小華",
    phone: "0923456789",
    preview: "請問有百合花嗎？想要一束",
    time: "2024-03-20 11:15"
  },
  {
    id: 3,
    customer_name: "張小美",
    phone: "0934567890",
    preview: "想要三束向日葵，可以加緞帶嗎？",
    time: "2024-03-20 13:45"
  }
];

export const mockStats = {
  today_orders: 5,
  pending_orders: 3,
  monthly_income: 15000,
  total_customers: 25
};

export const mockChatRooms = [
  {
    id: '1',
    name: '王小明',
    lastMessage: '好的，謝謝！',
    lastMessageTime: new Date(),
    unreadCount: 2
  },
  {
    id: '2',
    name: '李小華',
    lastMessage: '請問可以加卡片嗎？',
    lastMessageTime: new Date(Date.now() - 3600000),
    unreadCount: 0
  },
  {
    id: '3',
    name: '張小美',
    lastMessage: '我想要三束向日葵',
    lastMessageTime: new Date(Date.now() - 86400000),
    unreadCount: 1
  }
];

export const mockChatMessages = {
  "1": [
    {
      id: 1,
      sender: "王小明",
      text: "我想訂兩束玫瑰花",
      timestamp: new Date(Date.now() - 3600000),
      isSelf: false
    },
    {
      id: 2,
      sender: "我",
      text: "好的，請問預算多少？",
      timestamp: new Date(Date.now() - 3500000),
      isSelf: true
    },
    {
      id: 3,
      sender: "王小明",
      text: "預算2000元",
      timestamp: new Date(Date.now() - 3400000),
      isSelf: false
    },
    {
      id: 4,
      sender: "我",
      text: "沒問題，請問要自取還是外送？",
      timestamp: new Date(Date.now() - 3300000),
      isSelf: true
    },
    {
      id: 5,
      sender: "王小明",
      text: "自取，謝謝！",
      timestamp: new Date(Date.now() - 3200000),
      isSelf: false
    }
  ],
  "2": [
    {
      id: 1,
      sender: "李小華",
      text: "請問有百合花嗎？",
      timestamp: new Date(Date.now() - 7200000),
      isSelf: false
    },
    {
      id: 2,
      sender: "我",
      text: "有的，請問需要幾束？",
      timestamp: new Date(Date.now() - 7100000),
      isSelf: true
    },
    {
      id: 3,
      sender: "李小華",
      text: "一束就好，可以加卡片嗎？",
      timestamp: new Date(Date.now() - 7000000),
      isSelf: false
    }
  ],
  "3": [
    {
      id: 1,
      sender: "張小美",
      text: "我想要三束向日葵",
      timestamp: new Date(Date.now() - 86400000),
      isSelf: false
    },
    {
      id: 2,
      sender: "我",
      text: "好的，請問要加緞帶嗎？",
      timestamp: new Date(Date.now() - 86300000),
      isSelf: true
    },
    {
      id: 3,
      sender: "張小美",
      text: "要，謝謝！",
      timestamp: new Date(Date.now() - 86200000),
      isSelf: false
    }
  ]
}; 