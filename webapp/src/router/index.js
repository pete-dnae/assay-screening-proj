import Vue from 'vue';
import Router from 'vue-router';
import home from '@/pages/home/home.vue';
import platedesign from '@/pages/platedesign/platedesign.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/Home',
      name: 'Home',
      component: home,
    },
    {
      path: '/',
      name: 'platedesign',
      component: platedesign,
    },
  ],
});
