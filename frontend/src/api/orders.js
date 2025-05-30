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

export const createOrder_FromDraft = async (room_id) => {
  const res = await axios.post(`${API_BASE}/order/${room_id}`)
  return res.data
}

export const deleteOrder = async (order_id) => {
  const res = await axios.delete(`${API_BASE}/order/${order_id}`)
  return res.data
}

export const fetchOrderDraft = async (room_id) => {
  const res = await axios.patch(`${API_BASE}/organize_data/${room_id}`)
  return res.data
}

export const sendOrderDraft = async (room_id, order_draft) => {
  const res = await axios.patch(`${API_BASE}/orderdraft/${room_id}`, order_draft)
  return res.data
}

export const readOrderDraft = async (room_id) => {
  console.log('Reading order draft for room:', room_id)
  try {
    const res = await axios.get(`${API_BASE}/orderdraft/${room_id}`)
    console.log('Order draft read response:', res.data)
    return res.data
  } catch (error) {
    console.error('Error in readOrderDraft:', error)
    throw error
  }
}

export const exportDocx = async (order_id) => {
  try {
    const res = await axios.get(`${API_BASE}/orders/${order_id}.docx`, {
      responseType: 'blob' // Important for downloading files
    })
    return res.data
  } catch (error) {
    console.error('Error exporting docx:', error)
    throw error
  }
}