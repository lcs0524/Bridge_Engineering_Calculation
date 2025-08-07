import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      redirect: '/bridge-settlement',
    },
    {
      path: '/bridge-settlement',
      name: 'bridge-settlement',
      component: () => import('../views/BridgeSettlementView.vue')
    },
    {
      path: '/roadbed-calculation',
      name: 'roadbed-calculation',
      component: () => import('../views/RoadbedCalculationView.vue')
    },
    {
      path: '/foundation-stability',
      name: 'foundation-stability',
      component: () => import('../views/FoundationStabilityView.vue')
    }
  ]
})

export default router 