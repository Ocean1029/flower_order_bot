import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const isDevelopment = import.meta.env.DEV

export const getLatestMessages = async () => {
    const res = await axios.get(`${API_BASE}/chat_rooms`)
    return res.data
}

export const getRoomMessages = async (roomId) => {
    const res = await axios.get(`${API_BASE}/chat_rooms/${roomId}/messages`)
    return res.data
}

export const sendMessage = async (roomId, content) => {
    const res = await axios.post(`${API_BASE}/chat_rooms/${roomId}/messages`, {
        text: content,
        image_url: null
    })
    return res.data
}