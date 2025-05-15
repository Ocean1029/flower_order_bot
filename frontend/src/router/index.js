import { createRouter, createWebHistory } from 'vue-router'

// 頁面元件
import OrdersPage from '../pages/OrdersPage.vue'
import StatsPage from '../pages/StatsPage.vue'
import Dashboard from '../pages/Dashboard.vue'
import MessagePage from '../pages/MessagePage.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/orders', component: OrdersPage },
  { 
    path: '/messages', 
    component: MessagePage 
  },
  { path: '/stats', component: StatsPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
