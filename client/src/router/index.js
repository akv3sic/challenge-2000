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
    redirect: '/admin/planine',
    children: [
      {
        path: 'planine',
        name: 'mountains-list',
        component: () => import("@/views/backoffice/MountainsList")
      },
      // pojedinačna planina
      {
        path: 'planina/:id',
        name: 'mountain',
        component: () => import("@/views/backoffice/Mountain"),
        props: true
      },
      {
        path: 'korisnici',
        name: 'users-list',
        component: () => import("@/views/backoffice/UsersList")
      },
      // pojedinačni korisnik
      {
        path: 'korisnik/:id',
        name: 'user',
        component: () => import("@/views/backoffice/User"),
        props: true
      },
      {
        path: 'dodaj-novog-korisnika',
        name: 'users-add-new',
        component: () => import("@/views/backoffice/UsersAddNew")
      },
      {
        path: 'uredi-korisnika/:id',
        name: 'users-edit',
        component: () => import("@/views/backoffice/UsersEdit"),
        props: true
      },
      {
        path: 'drzave',
        name: 'states-list',
        component: () => import("@/views/backoffice/StatesList")
      },
    ]
  },
  //404 redirect
  {
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: () => import("@/views/NotFound")
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
