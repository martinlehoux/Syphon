import axios from 'axios'
import { checkToken } from '@/modules/auth'
import store from '@/store'

const http = axios.create({
  baseURL: `http://${window.location.hostname}:5000`,
  timeout: 5000,
  responseType: 'json'
})

http.interceptors.request.use(config => {
  const authorizationToken = localStorage.getItem('authorizationToken')
  if (checkToken(authorizationToken)) {
    config.headers['Authorization'] = `Bearer ${authorizationToken}`
  }
  return config
})

http.interceptors.response.use(res => {
  if (res.status === 498) {
    store.dispatch('logout')
  }
  return res
})

export default http
