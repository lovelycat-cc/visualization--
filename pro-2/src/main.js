// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import iView from 'iview'
import 'iview/dist/styles/iview.css'
Vue.use(iView)

Vue.prototype.$axios = axios
// eslint-disable-next-line
axios.defaults.baseURL = SERVICE_URL
Vue.config.productionTip = false

let color = {
  'civilization': '#ff7f0e',
  'economy': '#2ca02c',
  'education': '#d62728',
  'military': '#9467bd',
  'polity': '#1f77b4',
  'society': '#e377c2',
  'sports': '#7f7f7f',
  'other': '#bcbd22'
}
let labels = {
  'civilization': '人文',
  'economy': '经济',
  'education': '教育',
  'military': '军事',
  'polity': '政治',
  'society': '社会',
  'sports': '体育',
  'other': '其他'
}
Vue.prototype.scale = color
Vue.prototype.labelsObj = labels
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
