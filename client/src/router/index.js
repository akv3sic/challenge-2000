import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: "Home",
    redirect: '/admin/',
    component: () => import("@/views/backoffice/DashboardHome")
  },
  {
    path: '/admin/',
    name: "DashboardHome",
    component: () => import("@/views/backoffice/DashboardHome"),
    children: [
      {
        path: 'planine',
        name: 'mountains-list',
        component: () => import("@/views/backoffice/MountainsList")
      },
      {
        path: 'drzave',
        name: 'states-list',
        component: () => import("@/views/backoffice/StatesList")
      },
    ]
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
