// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import iView, {Notice} from 'iview'
import 'iview/dist/styles/iview.css'
Vue.use(iView)

Vue.prototype.$axios = axios
// eslint-disable-next-line
axios.defaults.baseURL = SERVICE_URL
Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  if (from.fullPath === '/lda' && !sessionStorage.getItem('allowJump')) {
    Notice.warning({
      title: '警告',
      desc: '当程序在运行，按钮处于等待状态时跳转可能导致该程序失效，关闭此弹窗即跳转，请谨慎操作！',
      duration: 0,
      onClose: () => {
        sessionStorage.setItem('allowJump', 'true')
        next({
          path: to.fullPath
        })
      }
    })
  } else {
    next()
    sessionStorage.setItem('allowJump', '')
  }
})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
