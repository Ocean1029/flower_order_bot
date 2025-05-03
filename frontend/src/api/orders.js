import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const fetchOrders = async () => {
  const res = await axios.get(`${API_BASE}/api/orders`)
  return res.data.orders
}
