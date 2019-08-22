import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Search from '@/views/Search'
import NewsList from '@/views/NewsList'

Vue.use(Router)

export default new Router({
  linkActiveClass: 'link-active',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    }, {
      path: '/searchPage',
      name: 'Search',
      component: Search
    }, {
      path: '/newsList',
      name: 'NewsList',
      component: NewsList
    }
  ]
})
