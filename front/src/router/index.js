import Vue from 'vue'
import VueRouter from 'vue-router'
import Admin from '@/views/Admin.vue'
import UserDetail from '@/views/UserDetail.vue'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Signup from '@/views/Signup.vue'
import store from '@/store'

Vue.use(VueRouter)

const openRoutes = ['/login', '/signup']

const routes = [
  {
    path: '/admin',
    component: Admin
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/signup',
    component: Signup
  },
  {
    path: '/users/:username',
    component: UserDetail
  },
  {
    path: '/',
    component: Home
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (localStorage.getItem('authorizationToken')) {
    store.dispatch('saveToken', localStorage.getItem('authorizationToken'))
  }
  if (openRoutes.includes(to.path) || store.state.loggedIn) {
    return next()
  } else {
    return next('/login')
  }
})

export default router
