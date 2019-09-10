import Vue from 'vue'
import App from './App.vue'
import router from './router'

import iView from 'iview';
import 'iview/dist/styles/iview.css';
Vue.use(iView);

import Upload from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(Upload);

Vue.config.productionTip = false

import http from './http';
Vue.prototype.$http = http;

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
