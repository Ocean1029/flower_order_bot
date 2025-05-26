import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const isDevelopment = import.meta.env.DEV

export const getLatestMessages = async () => {
    const res = await axios.get(`${API_BASE}/chat_rooms`)
    return res.data.map(room => ({
        id: room.room_id,
        name: room.user_name,
        lastMessage: room.last_message ? room.last_message.text : '',
        lastMessageTime: room.last_message ? new Date(room.last_message.timestamp) : null,
        unreadCount: room.unread_count,
        status: room.status,
        avatar: '' // You might want to add avatar to your API response
    }))
}

export const getRoomMessages = async (roomId) => {
    const res = await axios.get(`${API_BASE}/chat_rooms/${roomId}/messages`)
    return res.data
}

export const sendMessage = async (roomId, message) => {
    const res = await axios.post(`${API_BASE}/chat_rooms/${roomId}/messages`, message)
    return res.data
}