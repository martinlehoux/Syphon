import Vue from 'vue'
import axios from 'axios'
import SuiVue from 'semantic-ui-vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'

Vue.config.productionTip = false

Vue.prototype.$http = axios.create({
  baseURL: `http://${window.location.hostname}:5000`,
  timeout: 1000,
  responseType: 'json'
})

Vue.use(SuiVue)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
