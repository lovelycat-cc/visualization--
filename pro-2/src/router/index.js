import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import LDA from '@/views/LDA'

Vue.use(Router)

export default new Router({
  linkActiveClass: 'link-active',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/lda',
      name: 'lda',
      component: LDA
    }
  ]
})
