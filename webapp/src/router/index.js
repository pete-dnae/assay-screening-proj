import Vue from 'vue';
import Router from 'vue-router';

import experimenthome from '@/pages/experimenthome/experimenthome.vue';
import reagents from '@/pages/reagents';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/experiment/1',
    },
    {
      path: '/reagents',
      name: 'reagentHome',
      component: reagents,
    },
    {
      path: '/pools',
      name: 'reagentHome',
      component: reagents,
    },
    {
      path: '/experiment/:exptNo',
      name: 'experimenthome',
      component: experimenthome,
    },
  ],
});
