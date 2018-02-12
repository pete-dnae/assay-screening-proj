import Vue from 'vue';
import Router from 'vue-router';
import home from '@/pages/home/home.vue';
import platedesign from '@/pages/platedesign/platedesign.vue';
import experimenthome from '@/pages/experimenthome/experimenthome.vue';

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
      redirect: '/1',
    },
    {
      path: '/:expt/:plateId',
      name: 'platedesign',
      component: platedesign,
    },
    {
      path: '/:expt',
      name: 'experimenthome',
      component: experimenthome,
    },
  ],
});
