import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import axios from 'axios'

Vue.config.productionTip = false

Vue.prototype.$http = axios.create({
  baseURL: 'http://localhost:5000/',
  timeout: 1000,
  responseType: 'json'
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
