import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const getLatestMessages = async () => {
    const res = await axios.get(`${API_BASE}/api/messages`)
    return res.data.messages
}