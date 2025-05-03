import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const fetchStaticData = async () => {
  const res = await axios.get(`${API_BASE}/api/stats`)
  return res.data
}
