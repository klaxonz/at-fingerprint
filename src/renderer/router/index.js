import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'landing-page',
    //   component: require('@/components/LandingPage').default
    // },
    // {
    //   path: '/',
    //   name: 'login-page',
    //   component: require('@/components/LoginPage').default
    // },
    {
      path: '/',
      name: 'fringerprint-page',
      component: require('@/components/FingerPrintPage').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
