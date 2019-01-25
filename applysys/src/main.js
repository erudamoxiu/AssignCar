import Vue from 'vue'
import App from './App'
import router from './router'
import iView from 'iview';
import store from './store'
import 'iview/dist/styles/iview.css';
import request from '@/common/js/request.js'

Vue.use(iView);
Vue.config.productionTip = false

Vue.prototype.$userInfo = {
  userCode: '001',
  userName: 'admin'
}



localStorage.setItem('userInfo',{
  userid: '001',
  name: 'admin'
})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
