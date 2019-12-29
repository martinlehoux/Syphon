import Vue from 'vue'
import VueRouter from 'vue-router'
import UserList from '@/views/UserList.vue'
import UserDetail from '@/views/UserDetail.vue'
import RecordList from '@/views/RecordList.vue'
import Login from '@/views/Login.vue'
import store from '@/store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/users',
    component: UserList
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/users/:username',
    component: UserDetail
  },
  {
    path: '/records',
    component: RecordList
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.path === '/login' || store.state.loggedIn || localStorage.getItem('authorizationToken')) {
    return next()
  } else {
    return next('/login')
  }
})

export default router
