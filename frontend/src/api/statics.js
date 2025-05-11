import axios from 'axios'
import { mockApi } from './mockApi'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const isDevelopment = import.meta.env.DEV

export const fetchStaticData = async () => {
  if (isDevelopment) {
    return await mockApi.getStats()
  }
  
  const res = await axios.get(`${API_BASE}/api/stats`)
  return res.data
}