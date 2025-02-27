import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "../views/HomeView.vue"
// import ChatInterface from '../components/ChatInterface.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    // {
    //   path: '/chat',
    //   name: 'chat',
    //   component: ChatInterface,
    // },
  ],
})

export default router
