import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import AdminHome from '@/components/AdminHome'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'AdminHome',
      component: AdminHome
    }
  ]
})
