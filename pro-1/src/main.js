// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import iView from 'iview'
import 'iview/dist/styles/iview.css'
Vue.use(iView)

Vue.config.productionTip = false

let color = {
  0: '#ff7f0e',
  1: '#2ca02c',
  2: '#d62728',
  3: '#9467bd',
  4: '#1f77b4',
  5: '#e377c2',
  6: '#7f7f7f',
  7: '#bcbd22',
  8: '#17becf',
  9: '#1f77b4'
}

Vue.prototype.scale = color

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
