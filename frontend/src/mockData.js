export const mockOrders = [
  {
    id: 1,
    customer_name: "王小明",
    customer_phone: "0912345678",
    receipt_address: "台北市信義區信義路五段7號",
    order_date: "2024-03-20T10:30:00",
    total_amount: 2000,
    item: "玫瑰花束",
    quantity: 2,
    note: "紅色和白色各一束",
    pay_way: "Line Pay",
    card_message: "生日快樂！",
    weekday: "星期三",
    send_datetime: "2024-03-21T14:00:00",
    receiver_name: "李小華",
    receiver_phone: "0923456789",
    delivery_address: "台北市大安區復興南路一段390號",
    order_status: "confirmed",
    shipment_method: "delivery"
  },
  {
    id: 2,
    customer_name: "張小美",
    customer_phone: "0934567890",
    receipt_address: "台北市中山區南京東路三段219號",
    order_date: "2024-03-20T11:15:00",
    total_amount: 1500,
    item: "百合花束",
    quantity: 1,
    note: "要加緞帶",
    pay_way: "信用卡",
    card_message: "祝您開幕大吉",
    weekday: "星期四",
    send_datetime: "2024-03-21T15:30:00",
    receiver_name: "陳大明",
    receiver_phone: "0945678901",
    delivery_address: "台北市信義區松仁路100號",
    order_status: "pending",
    shipment_method: "store_pickup"
  },
  {
    id: 3,
    customer_name: "林小安",
    customer_phone: "0956789012",
    receipt_address: "台北市大安區敦化南路二段201號",
    order_date: "2024-03-20T13:45:00",
    total_amount: 3000,
    item: "向日葵花束",
    quantity: 3,
    note: "要加卡片",
    pay_way: "匯款",
    card_message: "母親節快樂",
    weekday: "星期五",
    send_datetime: "2024-03-22T10:00:00",
    receiver_name: "王媽媽",
    receiver_phone: "0967890123",
    delivery_address: "台北市信義區松高路68號",
    order_status: "completed",
    shipment_method: "delivery"
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
    unreadCount: 2,
    status: '人工溝通',
    avatar: 'https://randomuser.me/api/portraits/men/32.jpg'
  },
  {
    id: '2',
    name: '李小華',
    lastMessage: '請問可以加卡片嗎？',
    lastMessageTime: new Date(Date.now() - 3600000),
    unreadCount: 0,
    status: '人工溝通',
    avatar: 'https://randomuser.me/api/portraits/women/44.jpg'
  },
  {
    id: '3',
    name: '張小美',
    lastMessage: '我想要三束向日葵',
    lastMessageTime: new Date(Date.now() - 86400000),
    unreadCount: 1,
    status: '等待備貨',
    avatar: 'https://randomuser.me/api/portraits/women/68.jpg'
  },
  {
    id: '4',
    name: '陳大明',
    lastMessage: '自動回覆測試',
    lastMessageTime: new Date(Date.now() - 7200000),
    unreadCount: 3,
    status: '自動回覆',
    avatar: 'https://randomuser.me/api/portraits/men/12.jpg'
  },
  {
    id: '5',
    name: '林小安',
    lastMessage: '訂單已完成',
    lastMessageTime: new Date(Date.now() - 1800000),
    unreadCount: 0,
    status: '訂單完成',
    avatar: 'https://randomuser.me/api/portraits/men/56.jpg'
  }
];

export const mockChatMessages = {
  "1": [
    {
      id: 1,
      sender: "王小明",
      text: "我想訂兩束玫瑰花，預算2000元",
      timestamp: new Date(Date.now() - 3600000),
      direction: "incoming"
    },
    {
      id: 2,
      sender: "我",
      text: "好的，請問要什麼顏色？",
      timestamp: new Date(Date.now() - 3500000),
      direction: "outgoing_by_staff"
    },
    {
      id: 3,
      sender: "王小明",
      text: "紅色和白色都可以，謝謝！",
      timestamp: new Date(Date.now() - 3400000),
      direction: "incoming"
    },
    {
      id: 4,
      sender: "我",
      text: "沒問題，預計明天可取貨。",
      timestamp: new Date(Date.now() - 3300000),
      direction: "outgoing_by_staff"
    }
  ],
  "2": [
    {
      id: 1,
      sender: "李小華",
      text: "請問有百合花嗎？",
      timestamp: new Date(Date.now() - 7200000),
      direction: "incoming"
    },
    {
      id: 2,
      sender: "我",
      text: "有的，請問需要幾束？",
      timestamp: new Date(Date.now() - 7100000),
      direction: "outgoing_by_staff"
    },
    {
      id: 3,
      sender: "李小華",
      text: "一束就好，可以加卡片嗎？",
      timestamp: new Date(Date.now() - 7000000),
      direction: "incoming"
    },
    {
      id: 4,
      sender: "我",
      text: "可以，請問卡片內容？",
      timestamp: new Date(Date.now() - 6900000),
      direction: "outgoing_by_staff"
    }
  ],
  "3": [
    {
      id: 1,
      sender: "張小美",
      text: "我想要三束向日葵",
      timestamp: new Date(Date.now() - 86400000),
      direction: "incoming"
    },
    {
      id: 2,
      sender: "我",
      text: "好的，請問要加緞帶嗎？",
      timestamp: new Date(Date.now() - 86300000),
      direction: "outgoing_by_staff"
    },
    {
      id: 3,
      sender: "張小美",
      text: "要，謝謝！",
      timestamp: new Date(Date.now() - 86200000),
      direction: "incoming"
    },
    {
      id: 4,
      sender: "我",
      text: "預計明天下午可取貨喔。",
      timestamp: new Date(Date.now() - 86100000),
      direction: "outgoing_by_staff"
    }
  ],
  "4": [
    {
      id: 1,
      sender: "陳大明",
      text: "請問自動回覆是什麼？",
      timestamp: new Date(Date.now() - 7200000),
      direction: "incoming"
    },
    {
      id: 2,
      sender: "我",
      text: "您好，這是系統自動回覆，請稍等客服回覆您。",
      timestamp: new Date(Date.now() - 7190000),
      direction: "outgoing_by_staff"
    },
    {
      id: 3,
      sender: "陳大明",
      text: "好的，謝謝！",
      timestamp: new Date(Date.now() - 7180000),
      direction: "incoming"
    }
  ],
  "5": [
    {
      id: 1,
      sender: "林小安",
      text: "請問我的訂單什麼時候可以取？",
      timestamp: new Date(Date.now() - 1800000),
      direction: "incoming"
    },
    {
      id: 2,
      sender: "我",
      text: "預計明天下午三點後可取貨喔。",
      timestamp: new Date(Date.now() - 1700000),
      direction: "outgoing_by_staff"
    },
    {
      id: 3,
      sender: "林小安",
      text: "收到，謝謝你！",
      timestamp: new Date(Date.now() - 1600000),
      direction: "incoming"
    }
  ]
}; 