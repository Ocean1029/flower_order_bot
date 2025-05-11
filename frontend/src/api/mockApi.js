import { mockOrders, mockMessages, mockStats, mockChatRooms, mockChatMessages } from '../mockData';

// Simulate API delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const mockApi = {
  // Orders API
  async getOrders() {
    await delay(500); // Simulate network delay
    return { orders: mockOrders };
  },

  // Messages API
  async getMessages() {
    await delay(500);
    return { messages: mockMessages };
  },

  // Stats API
  async getStats() {
    await delay(500);
    return mockStats;
  },

  // Chat API
  async getChatRooms() {
    await delay(500);
    return mockChatRooms;
  },

  async getChatMessages(roomId) {
    await delay(500);
    return mockChatMessages[roomId] || [];
  },

  async sendMessage(roomId, message) {
    await delay(500);
    const newMessage = {
      id: Date.now(),
      sender: "我",
      text: message,
      timestamp: new Date(),
      isSelf: true
    };
    
    if (!mockChatMessages[roomId]) {
      mockChatMessages[roomId] = [];
    }
    mockChatMessages[roomId].push(newMessage);
    
    return newMessage;
  }
}; 