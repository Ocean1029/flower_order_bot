export const mockOrders = [
  {
    id: 1,
    customer_name: "王小明",
    phone: "0912345678",
    flower: "玫瑰花束",
    qty: 2,
    budget: 2000,
    pickup_method: "自取",
    pickup_date: "2024-03-20",
    pickup_time: "14:00",
    note: "要包裝漂亮一點"
  },
  {
    id: 2,
    customer_name: "李小華",
    phone: "0923456789",
    flower: "百合花束",
    qty: 1,
    budget: 1500,
    pickup_method: "外送",
    pickup_date: "2024-03-21",
    pickup_time: "15:30",
    note: "要加卡片"
  },
  {
    id: 3,
    customer_name: "張小美",
    phone: "0934567890",
    flower: "向日葵花束",
    qty: 3,
    budget: 3000,
    pickup_method: "自取",
    pickup_date: "2024-03-22",
    pickup_time: "16:00",
    note: "要加緞帶"
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
    id: "1",
    name: "王小明",
    lastMessage: "好的，謝謝！",
    lastMessageTime: new Date(),
    unreadCount: 0
  },
  {
    id: "2",
    name: "李小華",
    lastMessage: "請問可以加卡片嗎？",
    lastMessageTime: new Date(Date.now() - 3600000),
    unreadCount: 1
  },
  {
    id: "3",
    name: "張小美",
    lastMessage: "我想要三束向日葵",
    lastMessageTime: new Date(Date.now() - 86400000),
    unreadCount: 2
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