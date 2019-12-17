import Vue from 'vue'
import axios from 'axios'
import SuiVue from 'semantic-ui-vue'
import VueGoogleCharts from 'vue-google-charts'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'

Vue.config.productionTip = false

Vue.prototype.$http = axios.create({
  baseURL: `http://${window.location.hostname}:5000`,
  timeout: 5000,
  responseType: 'json'
})

Vue.use(SuiVue)
Vue.use(VueGoogleCharts)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
