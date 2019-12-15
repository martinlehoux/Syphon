import Vue from 'vue'
import VueRouter from 'vue-router'
import UserList from '@/views/UserList.vue'
import UserDetail from '@/views/UserDetail.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/users',
    component: UserList
  },
  {
    path: '/users/:username',
    component: UserDetail
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
