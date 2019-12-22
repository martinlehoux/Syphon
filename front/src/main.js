import Vue from 'vue'
import http from '@/modules/http'
import error from '@/modules/error'
import SuiVue from 'semantic-ui-vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'

Vue.config.productionTip = false

Vue.prototype.$http = http
Vue.prototype.$error = error

Vue.use(SuiVue)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
