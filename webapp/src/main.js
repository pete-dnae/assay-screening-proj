// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.css';
import '@/assets/sass/app.scss';
import 'bootstrap';
import { sync } from 'vuex-router-sync';
import jQuery from 'jquery';
import Vue from 'vue';
import App from './App';
import router from './router';
import store from './store';

Vue.config.productionTip = false;
window.$ = jQuery;
window.jQuery = jQuery;
sync(store, router);
/* eslint-disable no-new */

new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App },
});
