import axios from 'axios'
import { mockApi } from './mockApi'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const isDevelopment = import.meta.env.DEV

export const fetchOrders = async () => {
  if (isDevelopment) {
    const response = await mockApi.getOrders()
    return response.orders
  }
  
  const res = await axios.get(`${API_BASE}/api/orders`)
  return res.data.orders
}