import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import http from './plugins/http.js'

Vue.config.productionTip = false
Vue.prototype.$http = http

Vue.mixin({
  methods: {
    getAuthHeaders() {
      return {
        Authorization: `JWT ${localStorage.token || ''}`
      }
    }
  }
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
