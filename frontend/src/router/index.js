import { createRouter, createWebHistory } from 'vue-router'

// 頁面元件
import OrdersPage from '../pages/OrdersPage.vue'
import MessagesPage from '../pages/MessagesPage.vue'
import StatsPage from '../pages/StatsPage.vue'
import Dashboard from '../pages/Dashboard.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/orders', component: OrdersPage },
  { path: '/messages', component: MessagesPage },
  { path: '/stats', component: StatsPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
