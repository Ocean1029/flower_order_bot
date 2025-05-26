import axios from 'axios'


const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const isDevelopment = import.meta.env.DEV

export const fetchOrders = async () => {
  // if (isDevelopment) {
  //   const response = await mockApi.getOrders()
  //   return response.orders
  // }
  
  const res = await axios.get(`${API_BASE}/orders`)
  return res.data
}

export const fetchOrderDraft = async (room_id) => {
  const res = await axios.post(`${API_BASE}/organize_data/organize_data/${room_id}`)
  return res.data
}

