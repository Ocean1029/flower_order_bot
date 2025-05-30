import axios from 'axios'


const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const isDevelopment = import.meta.env.DEV

export const fetchStaticData = async () => {
  // if (isDevelopment) {
  //   return await mockApi.getStats()
  // }
  
  const res = await axios.get(`${API_BASE}/stats`)
  return res.data
}